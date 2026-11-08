use std::sync::Arc;
use tokio::sync::{mpsc, Mutex};

pub struct Supervisor {
    workers: Mutex<Vec<tokio::task::JoinHandle<()>>>,
    queue: mpsc::UnboundedSender<Job>,
}

pub async fn run(supervisor: Arc<Supervisor>, shutdown: tokio::sync::watch::Receiver<bool>) {
    let mut workers = supervisor.workers.lock().await;
    while let Some(worker) = workers.pop() {
        worker.abort();
    }
    drop(shutdown);
}
