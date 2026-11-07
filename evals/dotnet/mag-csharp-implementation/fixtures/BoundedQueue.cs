using System.Threading;
using System.Threading.Channels;
using System.Threading.Tasks;

namespace Fixture.Queueing;

/// <summary>
/// A bounded work queue with a single reader and multiple writers.
/// EnqueueAsync must:
///   1. wait (backpressure) while the queue is full, then enqueue when space opens;
///   2. throw OperationCanceledException promptly when the caller's token fires;
///   3. never enqueue after the queue has been marked complete.
/// </summary>
public sealed class BoundedWorkQueue<T>
{
    private readonly Channel<T> _channel;

    public BoundedWorkQueue(int capacity)
    {
        _channel = Channel.CreateBounded<T>(new BoundedChannelOptions(capacity)
        {
            FullMode = BoundedChannelFullMode.Wait,
            SingleReader = true,
            SingleWriter = false,
        });
    }

    public ChannelReader<T> Reader => _channel.Reader;

    public void Complete() => _channel.Writer.TryComplete();

    public async ValueTask EnqueueAsync(T item, CancellationToken cancellationToken)
    {
        // TODO: implement per the contract above.
        throw new System.NotImplementedException();
    }
}
