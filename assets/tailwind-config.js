/* WiseTrack — Aurora Engineering tokens (technical/futuristic).
   Deep midnight base, electric violet + cyan + indigo + acid lime. */
tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // Theme-aware: flip per :root vs html.light overrides in styles.css.
        // 'white' is overridden so border-white/X + bg-white/X scrim utilities
        // (used everywhere for HUD borders and glass surfaces) automatically
        // flip to black-with-alpha on light theme. --scrim = comma-RGB triplet
        // that swaps from "255, 255, 255" → "0, 0, 0".
        white: "rgba(var(--scrim), <alpha-value>)",
        bg: "var(--bg)",
        "bg-2": "var(--bg-2)",
        surface: "var(--surface)",
        "surface-2": "var(--surface-2)",
        "surface-3": "var(--surface-3)",
        line: "var(--line)",
        "line-2": "var(--line-2)",
        text: "var(--text)",
        "text-2": "var(--text-2)",
        muted: "var(--muted)",
        dim: "var(--dim)",
        // Curd & sindoor scales for Tailwind default colour names used across pages
        slate: {50: "#f2ebe5", 100: "#e9e0da", 200: "#d8c9c4", 300: "#c7b3ae", 400: "#b79d98", 500: "#a38581", 600: "#886968", 700: "#6d4d4f", 800: "#523236", 900: "#37161d", 950: "#2a0810"},
        gray: {50: "#f2ebe5", 100: "#e9e0da", 200: "#d8c9c4", 300: "#c7b3ae", 400: "#b79d98", 500: "#a38581", 600: "#886968", 700: "#6d4d4f", 800: "#523236", 900: "#37161d", 950: "#2a0810"},
        zinc: {50: "#f2ebe5", 100: "#e9e0da", 200: "#d8c9c4", 300: "#c7b3ae", 400: "#b79d98", 500: "#a38581", 600: "#886968", 700: "#6d4d4f", 800: "#523236", 900: "#37161d", 950: "#2a0810"},
        neutral: {50: "#f2ebe5", 100: "#e9e0da", 200: "#d8c9c4", 300: "#c7b3ae", 400: "#b79d98", 500: "#a38581", 600: "#886968", 700: "#6d4d4f", 800: "#523236", 900: "#37161d", 950: "#2a0810"},
        stone: {50: "#f2ebe5", 100: "#e9e0da", 200: "#d8c9c4", 300: "#c7b3ae", 400: "#b79d98", 500: "#a38581", 600: "#886968", 700: "#6d4d4f", 800: "#523236", 900: "#37161d", 950: "#2a0810"},
        indigo: {50: "#f9d7d3", 100: "#f5c2bd", 200: "#ed9992", 300: "#e66f67", 400: "#de453c", 500: "#d0241b", 600: "#b21e18", 700: "#931814", 800: "#741111", 900: "#550b0e", 950: "#46080c"},
        violet: {50: "#f9d7d3", 100: "#f5c2bd", 200: "#ed9992", 300: "#e66f67", 400: "#de453c", 500: "#d0241b", 600: "#b21e18", 700: "#931814", 800: "#741111", 900: "#550b0e", 950: "#46080c"},
        purple: {50: "#f9d7d3", 100: "#f5c2bd", 200: "#ed9992", 300: "#e66f67", 400: "#de453c", 500: "#d0241b", 600: "#b21e18", 700: "#931814", 800: "#741111", 900: "#550b0e", 950: "#46080c"},
        blue: {50: "#f9d7d3", 100: "#f5c2bd", 200: "#ed9992", 300: "#e66f67", 400: "#de453c", 500: "#d0241b", 600: "#b21e18", 700: "#931814", 800: "#741111", 900: "#550b0e", 950: "#46080c"},
        red: {50: "#f9d7d3", 100: "#f5c2bd", 200: "#ed9992", 300: "#e66f67", 400: "#de453c", 500: "#d0241b", 600: "#b21e18", 700: "#931814", 800: "#741111", 900: "#550b0e", 950: "#46080c"},
        rose: {50: "#f9d7d3", 100: "#f5c2bd", 200: "#ed9992", 300: "#e66f67", 400: "#de453c", 500: "#d0241b", 600: "#b21e18", 700: "#931814", 800: "#741111", 900: "#550b0e", 950: "#46080c"},
        pink: {50: "#f9d7d3", 100: "#f5c2bd", 200: "#ed9992", 300: "#e66f67", 400: "#de453c", 500: "#d0241b", 600: "#b21e18", 700: "#931814", 800: "#741111", 900: "#550b0e", 950: "#46080c"},
        fuchsia: {50: "#f9d7d3", 100: "#f5c2bd", 200: "#ed9992", 300: "#e66f67", 400: "#de453c", 500: "#d0241b", 600: "#b21e18", 700: "#931814", 800: "#741111", 900: "#550b0e", 950: "#46080c"},
        sky: {50: "#f3e8cd", 100: "#ecddbd", 200: "#dec99b", 300: "#d0b47a", 400: "#c29f58", 500: "#b28b3d", 600: "#9b7933", 700: "#846629", 800: "#6d531f", 900: "#564015", 950: "#4a3710"},
        cyan: {50: "#f3e8cd", 100: "#ecddbd", 200: "#dec99b", 300: "#d0b47a", 400: "#c29f58", 500: "#b28b3d", 600: "#9b7933", 700: "#846629", 800: "#6d531f", 900: "#564015", 950: "#4a3710"},
        emerald: {50: "#d8e5d0", 100: "#c8d9bf", 200: "#a8bf9b", 300: "#87a678", 400: "#678d55", 500: "#4c7638", 600: "#426832", 700: "#38592b", 800: "#2d4a24", 900: "#233b1d", 950: "#1e341a"},
        green: {50: "#d8e5d0", 100: "#c8d9bf", 200: "#a8bf9b", 300: "#87a678", 400: "#678d55", 500: "#4c7638", 600: "#426832", 700: "#38592b", 800: "#2d4a24", 900: "#233b1d", 950: "#1e341a"},
        teal: {50: "#d8e5d0", 100: "#c8d9bf", 200: "#a8bf9b", 300: "#87a678", 400: "#678d55", 500: "#4c7638", 600: "#426832", 700: "#38592b", 800: "#2d4a24", 900: "#233b1d", 950: "#1e341a"},
        amber: {50: "#f3e8cd", 100: "#ecddbd", 200: "#dec99b", 300: "#d0b47a", 400: "#c29f58", 500: "#b28b3d", 600: "#9b7933", 700: "#846629", 800: "#6d531f", 900: "#564015", 950: "#4a3710"},
        yellow: {50: "#f3e8cd", 100: "#ecddbd", 200: "#dec99b", 300: "#d0b47a", 400: "#c29f58", 500: "#b28b3d", 600: "#9b7933", 700: "#846629", 800: "#6d531f", 900: "#564015", 950: "#4a3710"},
        orange: {50: "#f3e8cd", 100: "#ecddbd", 200: "#dec99b", 300: "#d0b47a", 400: "#c29f58", 500: "#b28b3d", 600: "#9b7933", 700: "#846629", 800: "#6d531f", 900: "#564015", 950: "#4a3710"},
        // Primary accent system
        violet: "#d8261c",
        "violet-2": "#ff6a45",
        indigo: "#c9301f",
        sky: "#c9a55a",
        cyan: "#d9b26a",
        lime: "#9fd3a6",
        mint: "#7fc08a",
        steel: "#b59a95",
        // legacy aliases (kept so previously-used utility classes still resolve)
        fuchsia: "#c9301f",
        pink: "#c9a55a",
        ember: "#b59a95"
      },
      fontFamily: {
        display: ['"Fraunces"', "ui-serif", "Georgia", "serif"],
        sans: ['"Inter Tight"', "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ['"JetBrains Mono"', "ui-monospace", "monospace"]
      },
      letterSpacing: {
        ticker: "0.28em",
        slug: "0.22em",
        wider2: "0.18em"
      },
      maxWidth: { page: "1440px", prose: "62ch" },
      spacing: {
        edge: "clamp(1.25rem, 4vw, 4.5rem)",
        gutter: "clamp(1rem, 2vw, 1.75rem)"
      },
      boxShadow: {
        glow: "0 0 60px -10px rgba(216,38,28,0.45), 0 0 100px -20px rgba(184,144,63,0.25)",
        "glow-sm": "0 0 24px -4px rgba(216,38,28,0.4)",
        card: "0 1px 0 0 rgba(255,255,255,0.04), 0 24px 60px -30px rgba(0,0,0,0.6)",
        inset: "inset 0 1px 0 0 rgba(255,255,255,0.06)"
      },
      backgroundImage: {
        "grid-dots":
          "radial-gradient(rgba(255,255,255,0.06) 1px, transparent 1px)",
        aurora:
          "conic-gradient(from 180deg at 50% 50%, #d8261c 0deg, #c9301f 90deg, #d9b26a 200deg, #c9a55a 300deg, #d8261c 360deg)"
      },
      keyframes: {
        rise: {
          "0%": { opacity: 0, transform: "translateY(18px)" },
          "100%": { opacity: 1, transform: "translateY(0)" }
        },
        slide: {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(-50%)" }
        },
        blink: {
          "0%,49%": { opacity: 1 },
          "50%,100%": { opacity: 0.25 }
        },
        drift: {
          "0%,100%": { transform: "translate3d(0,0,0) scale(1)" },
          "33%": { transform: "translate3d(4%,-6%,0) scale(1.05)" },
          "66%": { transform: "translate3d(-3%,4%,0) scale(0.97)" }
        },
        spin: { to: { transform: "rotate(360deg)" } },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" }
        }
      },
      animation: {
        rise: "rise 800ms cubic-bezier(0.2,0.7,0.2,1) both",
        ticker: "slide 48s linear infinite",
        blink: "blink 1.4s steps(1) infinite",
        drift: "drift 22s ease-in-out infinite",
        "spin-slow": "spin 28s linear infinite",
        shimmer: "shimmer 3.2s linear infinite"
      }
    }
  }
};
