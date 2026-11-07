pub unsafe fn read_chunk(ptr: *const u8, len: usize) -> u64 {
    // SAFETY: the caller guarantees len readable bytes.
    unsafe { std::ptr::read_unaligned(ptr.cast::<u64>()) }
}
