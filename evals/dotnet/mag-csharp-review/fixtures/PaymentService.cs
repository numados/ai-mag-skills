using System;
using System.IO;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

namespace Fixture.Payments;

public sealed class Money : IEquatable<Money>
{
    public Money(string currency, decimal amount)
    {
        Currency = currency;
        Amount = amount;
    }

    public string Currency { get; }
    public decimal Amount { get; }

    public bool Equals(Money? other) =>
        other is not null && Currency == other.Currency && Amount == other.Amount;

    public override bool Equals(object? obj) => Equals(obj as Money);

    // GetHashCode is not overridden, so two equal Money values can hash
    // differently and never be found in a Dictionary or HashSet.
}

public sealed class PaymentClient : IDisposable
{
    private readonly HttpClient _http = new();

    public async Task<string> GetReceiptAsync(string id, CancellationToken ct) =>
        await _http.GetStringAsync($"/payments/{id}/receipt", ct);

    public string GetReceipt(string id)
    {
        // sync-over-async on a request path: blocks a thread and can deadlock.
        return _http.GetStringAsync($"/payments/{id}/receipt").Result;
    }

    public void Dispose() => _http.Dispose();
}

public sealed class ReceiptRepository
{
    public string LoadReceipt(MemoryStream buffer)
    {
        var reader = new StreamReader(buffer, leaveOpen: false);
        var text = reader.ReadToEnd();
        reader.Dispose();
        return reader.ReadToEnd(); // reuse after dispose: throws ObjectDisposedException.
    }
}
