using System;

namespace Fixture.Timekeeping;

/// <summary>
/// Coupon expiry depends on the current time. Tests must be deterministic,
/// so the service consumes TimeProvider and tests inject FakeTimeProvider
/// instead of relying on wall-clock time or Thread.Sleep.
/// </summary>
public sealed class CouponService
{
    private readonly TimeProvider _time;

    public CouponService(TimeProvider time)
    {
        _time = time;
    }

    public bool IsExpired(DateTimeOffset expiresAt) =>
        _time.GetUtcNow() >= expiresAt;
}
