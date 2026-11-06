pub fn parse(input: &str) -> Result<u32, ParseError> {
    input.parse().map_err(ParseError::from)
}
