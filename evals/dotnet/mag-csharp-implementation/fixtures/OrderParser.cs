using System;

public sealed class OrderParser
{
    public ParsedOrder Parse(string? input)
    {
        var parts = input.Split(';');
        var id = int.Parse(parts[0]);
        var quantity = int.Parse(parts[1]);
        return new ParsedOrder(id, quantity);
    }
}

public readonly record struct ParsedOrder(int Id, int Quantity);
