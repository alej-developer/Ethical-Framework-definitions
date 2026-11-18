/** EN: HTML escaping utility for safe interpolation of untrusted API data into innerHTML templates. | ES: Utilidad de escape HTML para interpolacion segura de datos de API no confiables en plantillas innerHTML. */

const HTML_ESCAPE_MAP: Record<string, string> = {
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  '"': "&quot;",
  "'": "&#39;",
};

export function escapeHtml(value: unknown): string {
  // EN: Convert value to string and escape special HTML characters | ES: Convertir valor a cadena y escapar caracteres HTML especiales
  if (value === null || value === undefined) {
    return "";
  }
  return String(value).replace(/[&<>"']/g, (char) => HTML_ESCAPE_MAP[char] ?? char);
}
