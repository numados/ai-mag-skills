// Synthetic fixture; no real vendor dependency is installed.
import { cache } from "./services.js";

export function report(id, tier, load) {
  return cache.remember("report:" + tier + ":" + id, load, { ttlSeconds: 300 });
}

export function preview(id, tier, load) {
  return cache.remember("preview:" + tier + ":" + id, load, { ttlSeconds: 300 });
}
