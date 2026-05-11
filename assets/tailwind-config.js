/* WiseTrack — Aurora Engineering tokens (technical/futuristic).
   Deep midnight base, electric violet + cyan + indigo + acid lime. */
tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        bg: "#07070C",
        "bg-2": "#0A0A12",
        surface: "#0E0F18",
        "surface-2": "#15161F",
        "surface-3": "#1B1D29",
        line: "#23253A",
        "line-2": "#2F3247",
        text: "#EDEAF7",
        "text-2": "#C6C2D8",
        muted: "#9692B0",
        dim: "#5E5A77",
        // Primary accent system
        violet: "#7C3AED",
        "violet-2": "#A78BFA",
        indigo: "#6366F1",
        sky: "#38BDF8",
        cyan: "#22D3EE",
        lime: "#BEF264",
        mint: "#34D399",
        steel: "#94A3B8",
        // legacy aliases (kept so previously-used utility classes still resolve)
        fuchsia: "#6366F1",
        pink: "#38BDF8",
        ember: "#94A3B8"
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
        glow: "0 0 60px -10px rgba(124,58,237,0.45), 0 0 100px -20px rgba(34,211,238,0.25)",
        "glow-sm": "0 0 24px -4px rgba(124,58,237,0.4)",
        card: "0 1px 0 0 rgba(255,255,255,0.04), 0 24px 60px -30px rgba(0,0,0,0.6)",
        inset: "inset 0 1px 0 0 rgba(255,255,255,0.06)"
      },
      backgroundImage: {
        "grid-dots":
          "radial-gradient(rgba(255,255,255,0.06) 1px, transparent 1px)",
        aurora:
          "conic-gradient(from 180deg at 50% 50%, #7C3AED 0deg, #6366F1 90deg, #22D3EE 200deg, #38BDF8 300deg, #7C3AED 360deg)"
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
