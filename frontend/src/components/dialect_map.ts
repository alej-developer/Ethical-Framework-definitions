/** EN: Lazy-loaded static SVG broad-region map for documented linguistic varieties (Natural Earth 110m Public Domain simplified geometry, zero external services). | ES: Mapa SVG estatico de carga diferida por regiones amplias para variedades linguisticas documentadas (geometria simplificada Natural Earth 110m de dominio publico, sin servicios externos). */

import { getTranslation, Translations } from "../i18n/translations.ts";
import { Language, LinguisticArtifact } from "../types/index.ts";
import { escapeHtml } from "../utils/escape_html.ts";

interface RegionGeometry {
  code: "US" | "NG" | "GB";
  labelKey: keyof Translations;
  path: string;
}

// EN: Simplified broad-region silhouettes derived from Natural Earth 110m (Public Domain / CC0), Equirectangular projection 800x380 | ES: Siluetas simplificadas de regiones amplias derivadas de Natural Earth 110m (Dominio Publico / CC0), proyeccion equirectangular 800x380
const CONTINENT_SILHOUETTES: string[] = [
  // North & Central America
  "M 45,55 L 185,35 L 270,58 L 252,98 L 222,126 L 190,152 L 175,182 L 152,188 L 136,162 L 106,138 L 88,96 L 45,78 Z",
  // South America
  "M 188,195 L 244,195 L 285,232 L 268,288 L 225,352 L 204,352 L 194,284 L 180,235 Z",
  // Europe
  "M 366,78 L 435,54 L 486,62 L 482,102 L 452,118 L 410,124 L 372,116 L 366,95 Z",
  // Africa
  "M 364,132 L 444,130 L 492,168 L 478,242 L 442,312 L 414,312 L 392,248 L 352,196 L 352,155 Z",
  // Asia
  "M 484,52 L 668,46 L 748,74 L 725,134 L 682,168 L 636,192 L 585,196 L 542,175 L 492,150 L 478,104 Z",
  // Oceania
  "M 642,244 L 724,244 L 740,298 L 692,318 L 642,292 Z",
];

const BROAD_REGIONS: RegionGeometry[] = [
  {
    code: "US",
    labelKey: "regionUSLabel",
    path: "M 102,94 L 228,94 L 220,128 L 192,142 L 134,138 L 104,120 Z",
  },
  {
    code: "GB",
    labelKey: "regionGBLabel",
    path: "M 364,76 L 386,74 L 388,96 L 366,98 Z",
  },
  {
    code: "NG",
    labelKey: "regionNGLabel",
    path: "M 398,172 L 424,172 L 426,194 L 400,196 Z",
  },
];

export function renderDialectMap(
  container: HTMLElement,
  artifacts: LinguisticArtifact[],
  selectedIndex: number | null,
  lang: Language,
  onSelectArtifact: (index: number) => void,
): void {
  const geoArtifacts = artifacts
    .map((artifact, index) => ({ artifact, index }))
    .filter(({ artifact }) => Boolean(artifact.geographic_region));

  const nonGeoArtifacts = artifacts
    .map((artifact, index) => ({ artifact, index }))
    .filter(({ artifact }) => !artifact.geographic_region);

  const selectedRegion =
    selectedIndex !== null ? artifacts[selectedIndex]?.geographic_region ?? null : null;

  const regionShapes = BROAD_REGIONS.map((region) => {
    const matches = geoArtifacts.filter(({ artifact }) => artifact.geographic_region === region.code);
    const isPresent = matches.length > 0;
    const hasDisparity = matches.some(
      ({ artifact }) => artifact.observed_output !== artifact.expected_output,
    );
    const isSelected = selectedRegion === region.code;

    let stateClass = "map-region-inactive";
    if (isPresent) {
      stateClass = hasDisparity ? "map-region-disparity" : "map-region-aligned";
    }
    if (isSelected) {
      stateClass += " map-region-selected";
    }

    const label = getTranslation(region.labelKey, lang);
    const varietiesSummary = matches.map(({ artifact }) => artifact.dialect_or_variety).join(", ");
    const ariaLabel = isPresent ? `${label}: ${varietiesSummary}` : label;

    if (!isPresent) {
      return `<path class="map-region ${stateClass}" d="${region.path}" aria-hidden="true" />`;
    }

    return `
      <path
        class="map-region map-region-interactive ${stateClass}"
        d="${region.path}"
        data-region="${region.code}"
        role="button"
        tabindex="0"
        aria-pressed="${isSelected ? "true" : "false"}"
        aria-label="${escapeHtml(ariaLabel)}"
      >
        <title>${escapeHtml(ariaLabel)}</title>
      </path>
    `;
  }).join("");

  const geoLegendItems = geoArtifacts
    .map(({ artifact, index }) => {
      const regionMeta = BROAD_REGIONS.find((r) => r.code === artifact.geographic_region);
      const regionName = regionMeta ? getTranslation(regionMeta.labelKey, lang) : artifact.geographic_region;
      const isSelected = index === selectedIndex;
      const isMismatch = artifact.observed_output !== artifact.expected_output;
      return `
        <button
          type="button"
          class="map-variety-item ${isSelected ? "selected" : ""}"
          data-artifact-index="${index}"
          aria-pressed="${isSelected ? "true" : "false"}"
        >
          <span class="map-variety-header">
            <strong class="map-variety-name">${escapeHtml(artifact.dialect_or_variety)}</strong>
            <span class="status-badge ${isMismatch ? "mismatch" : "match"}">${escapeHtml(regionName)}</span>
          </span>
          ${
            artifact.geographic_source
              ? `<span class="map-variety-source">${getTranslation("geographicSourceLabel", lang)}: ${escapeHtml(artifact.geographic_source)}</span>`
              : ""
          }
        </button>
      `;
    })
    .join("");

  const nonGeoSection =
    nonGeoArtifacts.length > 0
      ? `
      <div class="non-geo-registers">
        <span class="map-sub-label">${getTranslation("nonGeographicRegistersLabel", lang)}</span>
        <div class="non-geo-list">
          ${nonGeoArtifacts
            .map(({ artifact, index }) => {
              const isSelected = index === selectedIndex;
              return `
                <button
                  type="button"
                  class="map-variety-item ${isSelected ? "selected" : ""}"
                  data-artifact-index="${index}"
                  aria-pressed="${isSelected ? "true" : "false"}"
                >
                  <span class="map-variety-header">
                    <strong class="map-variety-name">${escapeHtml(artifact.dialect_or_variety)}</strong>
                    <span class="meta-chip">${escapeHtml(artifact.protected_attribute)}</span>
                  </span>
                </button>
              `;
            })
            .join("")}
        </div>
      </div>
    `
      : "";

  container.innerHTML = `
    <div class="dialect-map-panel">
      <p class="map-note">${getTranslation("dialectMapNote", lang)}</p>
      ${
        geoArtifacts.length > 0
          ? `
        <div class="dialect-svg-frame">
          <svg
            class="dialect-world-svg"
            viewBox="0 0 800 380"
            role="img"
            aria-label="${escapeHtml(getTranslation("dialectMapHeading", lang))}"
          >
            <g class="map-continents" aria-hidden="true">
              ${CONTINENT_SILHOUETTES.map((d) => `<path class="map-continent-path" d="${d}" />`).join("")}
            </g>
            <g class="map-broad-regions">
              ${regionShapes}
            </g>
          </svg>
        </div>
        <div class="map-variety-list">
          ${geoLegendItems}
        </div>
      `
          : ""
      }
      ${nonGeoSection}
    </div>
  `;

  // EN: Synchronize map region clicks/keys with artifact selection | ES: Sincronizar clics y teclado de regiones del mapa con la seleccion de artefactos
  container.querySelectorAll<SVGPathElement>(".map-region-interactive").forEach((regionEl) => {
    const activateRegion = (): void => {
      const regionCode = regionEl.getAttribute("data-region");
      const matchingIndices = geoArtifacts
        .filter(({ artifact }) => artifact.geographic_region === regionCode)
        .map(({ index }) => index);
      if (matchingIndices.length === 0) return;

      const currentPos = selectedIndex !== null ? matchingIndices.indexOf(selectedIndex) : -1;
      const nextIndex = matchingIndices[(currentPos + 1) % matchingIndices.length];
      onSelectArtifact(nextIndex);
    };

    regionEl.addEventListener("click", activateRegion);
    regionEl.addEventListener("keydown", (event: KeyboardEvent) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        activateRegion();
      }
    });
  });

  container.querySelectorAll<HTMLButtonElement>(".map-variety-item").forEach((btn) => {
    btn.addEventListener("click", () => {
      const idx = Number(btn.getAttribute("data-artifact-index"));
      if (!Number.isNaN(idx)) {
        onSelectArtifact(idx);
      }
    });
  });
}
