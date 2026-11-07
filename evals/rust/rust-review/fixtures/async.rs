async fn write_serialized(writer: &tokio::sync::Mutex<Writer>) -> std::io::Result<()> {
    let mut writer = writer.lock().await;
    writer.write_all(b"header").await
}
