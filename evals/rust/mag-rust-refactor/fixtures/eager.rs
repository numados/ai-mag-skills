use std::cell::Cell;

pub fn eager(xs: &[u32], calls: &Cell<usize>) -> Option<u32> {
    let values: Vec<u32> = xs.iter().map(|x| {
        calls.set(calls.get() + 1);
        *x + 1
    }).collect();
    values.first().copied()
}

pub fn lazy(xs: &[u32], calls: &Cell<usize>) -> Option<u32> {
    xs.iter().map(|x| {
        calls.set(calls.get() + 1);
        *x + 1
    }).next()
}
