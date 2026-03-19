/** Format yen price — shows as ¥2,500,000 or ¥250万 */
export function formatPrice(yen: number): string {
  if (yen >= 10_000) {
    const man = yen / 10_000;
    return `¥${man % 1 === 0 ? man.toFixed(0) : man.toFixed(1)}万`;
  }
  return `¥${yen.toLocaleString()}`;
}

/** Format km with thousand separator */
export function formatMileage(km: number): string {
  return `${km.toLocaleString()} km`;
}

/** Format engine displacement */
export function formatEngine(cc: number | null): string {
  if (!cc) return "—";
  return cc >= 1000 ? `${(cc / 1000).toFixed(1)}L` : `${cc}cc`;
}

/** Shorten a long dealer / prefecture name to fit in a card */
export function truncate(text: string, max = 24): string {
  return text.length > max ? `${text.slice(0, max)}…` : text;
}
