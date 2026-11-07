using System.Threading;
using Microsoft.EntityFrameworkCore;

namespace Fixture.Tenancy;

public sealed class TenantDbContext : DbContext
{
    private readonly string _tenantId;

    public TenantDbContext(DbContextOptions<TenantDbContext> options) : base(options)
    {
        // Defect: when this context is pooled via AddDbContextPool, the
        // constructor runs once per pooled instance and cannot carry a
        // per-request tenant. Tenant state read here leaks across requests.
        _tenantId = CurrentTenant.Value ?? "unknown";
    }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        // Defect: OnConfiguring also runs once per pooled instance, so it
        // cannot set per-request state such as the tenant id.
        base.OnConfiguring(optionsBuilder);
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Order>().HasQueryFilter(o => o.TenantId == _tenantId);
    }

    public DbSet<Order> Orders => Set<Order>();

    // Illustrative ambient tenant accessor; the real defect is reading it in
    // the constructor/OnConfiguring of a pooled context.
    public static AsyncLocal<string?> CurrentTenant { get; } = new();
}

public sealed class Order
{
    public int Id { get; set; }
    public string TenantId { get; set; } = string.Empty;
}
