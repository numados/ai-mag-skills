use std::sync::Arc;
use tokio::sync::{mpsc, Mutex, Semaphore};

#[derive(Debug)]
pub struct Job {
    pub id: u64,
    pub payload: String,
}

pub async fn supervisor(mut input: tokio::sync::mpsc::Receiver<Job>) {
    let permits = Arc::new(Semaphore::new(4));
    let state = Arc::new(Mutex::new(State { processed: 0 }));
    while let Some(job) = input.recv().await {
        let permits = permits.clone();
        let state = state.clone();
        tokio::spawn(async move {
            let permit = permits.acquire_owned().await.unwrap();
            let result = tokio::task::spawn_blocking(move || process(job)).await;
            if result.is_ok() {
                let mut guard = state.lock().await;
                guard.processed += 1;
            }
        });
    }
}

pub async fn bump(state: &tokio::sync::Mutex<State>) {
    let mut guard = state.lock().await;
    guard.processed += 1;
}

pub struct State {
    pub processed: u64,
}

pub fn process(job: Job) -> u64 {
    job.id
}
