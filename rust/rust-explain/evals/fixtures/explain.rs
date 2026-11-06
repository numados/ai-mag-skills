pub fn parse(raw: &str) -> Result<u16, std::num::ParseIntError> {
    let n = raw.parse()?;
    Ok(n)
}

pub fn first(raw: Option<&str>) -> Option<u16> {
    let text = raw?;
    text.parse().ok()
}
