pub unsafe fn read_u64(ptr: *const u8, len: usize) -> u64 {
    // SAFETY: caller provides len readable bytes.
    unsafe { std::ptr::read_unaligned(ptr.cast::<u64>()) }
}
