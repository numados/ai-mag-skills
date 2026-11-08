//! Soundness review fixture: a guard whose auto-trait bound is suspect.
//! The lock/unlock orderings themselves are assumed correct in this exercise.
use std::{
    cell::{Cell, UnsafeCell},
    ops::Deref,
    sync::atomic::{AtomicBool, AtomicU64, Ordering},
};

pub struct Lock<T> {
    held: AtomicBool,
    value: UnsafeCell<T>,
}

pub struct Guard<'a, T> {
    value: &'a T,
}

impl<T> Deref for Guard<'_, T> {
    type Target = T;
    fn deref(&self) -> &T {
        self.value
    }
}

// SAFETY: `acquire` grants exclusive access while the guard is alive.
unsafe impl<T: Send> Sync for Guard<'_, T> {}

impl<T: Send> Lock<T> {
    pub fn new(value: T) -> Self {
        Self { held: AtomicBool::new(false), value: UnsafeCell::new(value) }
    }

    pub fn acquire(&self) -> Option<Guard<'_, T>> {
        let won = self
            .held
            .compare_exchange(false, true, Ordering::Acquire, Ordering::Relaxed)
            .is_ok();
        if won {
            // SAFETY: guarded by `held`; released in `release`.
            Some(Guard { value: unsafe { &*self.value.get() } })
        } else {
            None
        }
    }

    pub fn release(&self) {
        self.held.store(false, Ordering::Release);
    }
}

static JOBS: AtomicU64 = AtomicU64::new(0);
static ERRORS: AtomicU64 = AtomicU64::new(0);

pub fn metric() {
    JOBS.fetch_add(1, Ordering::Relaxed);
    ERRORS.fetch_add(1, Ordering::Relaxed);
}

pub fn demo() -> u8 {
    let lock = Lock::new(Cell::new(0u8));
    if let Some(guard) = lock.acquire() {
        guard.value.set(guard.value.get() + 1);
    }
    lock.release();
    metric();
    lock.acquire().map(|g| g.value.get()).unwrap_or(0)
}
