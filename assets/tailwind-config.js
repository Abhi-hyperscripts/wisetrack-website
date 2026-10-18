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
        slate: {50: "rgb(var(--taupe-94d-rgb) / <alpha-value>)", 100: "rgb(var(--taupe-91c-rgb) / <alpha-value>)", 200: "rgb(var(--taupe-85-rgb) / <alpha-value>)", 300: "rgb(var(--taupe-78-rgb) / <alpha-value>)", 400: "rgb(var(--taupe-72-rgb) / <alpha-value>)", 500: "rgb(var(--taupe-64-rgb) / <alpha-value>)", 600: "rgb(var(--taupe-55-rgb) / <alpha-value>)", 700: "rgb(var(--taupe-46-rgb) / <alpha-value>)", 800: "rgb(var(--taupe-36-rgb) / <alpha-value>)", 900: "rgb(var(--taupe-25-rgb) / <alpha-value>)", 950: "rgb(var(--taupe-20-rgb) / <alpha-value>)"},
        gray: {50: "rgb(var(--taupe-94d-rgb) / <alpha-value>)", 100: "rgb(var(--taupe-91c-rgb) / <alpha-value>)", 200: "rgb(var(--taupe-85-rgb) / <alpha-value>)", 300: "rgb(var(--taupe-78-rgb) / <alpha-value>)", 400: "rgb(var(--taupe-72-rgb) / <alpha-value>)", 500: "rgb(var(--taupe-64-rgb) / <alpha-value>)", 600: "rgb(var(--taupe-55-rgb) / <alpha-value>)", 700: "rgb(var(--taupe-46-rgb) / <alpha-value>)", 800: "rgb(var(--taupe-36-rgb) / <alpha-value>)", 900: "rgb(var(--taupe-25-rgb) / <alpha-value>)", 950: "rgb(var(--taupe-20-rgb) / <alpha-value>)"},
        zinc: {50: "rgb(var(--taupe-94d-rgb) / <alpha-value>)", 100: "rgb(var(--taupe-91c-rgb) / <alpha-value>)", 200: "rgb(var(--taupe-85-rgb) / <alpha-value>)", 300: "rgb(var(--taupe-78-rgb) / <alpha-value>)", 400: "rgb(var(--taupe-72-rgb) / <alpha-value>)", 500: "rgb(var(--taupe-64-rgb) / <alpha-value>)", 600: "rgb(var(--taupe-55-rgb) / <alpha-value>)", 700: "rgb(var(--taupe-46-rgb) / <alpha-value>)", 800: "rgb(var(--taupe-36-rgb) / <alpha-value>)", 900: "rgb(var(--taupe-25-rgb) / <alpha-value>)", 950: "rgb(var(--taupe-20-rgb) / <alpha-value>)"},
        neutral: {50: "rgb(var(--taupe-94d-rgb) / <alpha-value>)", 100: "rgb(var(--taupe-91c-rgb) / <alpha-value>)", 200: "rgb(var(--taupe-85-rgb) / <alpha-value>)", 300: "rgb(var(--taupe-78-rgb) / <alpha-value>)", 400: "rgb(var(--taupe-72-rgb) / <alpha-value>)", 500: "rgb(var(--taupe-64-rgb) / <alpha-value>)", 600: "rgb(var(--taupe-55-rgb) / <alpha-value>)", 700: "rgb(var(--taupe-46-rgb) / <alpha-value>)", 800: "rgb(var(--taupe-36-rgb) / <alpha-value>)", 900: "rgb(var(--taupe-25-rgb) / <alpha-value>)", 950: "rgb(var(--taupe-20-rgb) / <alpha-value>)"},
        stone: {50: "rgb(var(--taupe-94d-rgb) / <alpha-value>)", 100: "rgb(var(--taupe-91c-rgb) / <alpha-value>)", 200: "rgb(var(--taupe-85-rgb) / <alpha-value>)", 300: "rgb(var(--taupe-78-rgb) / <alpha-value>)", 400: "rgb(var(--taupe-72-rgb) / <alpha-value>)", 500: "rgb(var(--taupe-64-rgb) / <alpha-value>)", 600: "rgb(var(--taupe-55-rgb) / <alpha-value>)", 700: "rgb(var(--taupe-46-rgb) / <alpha-value>)", 800: "rgb(var(--taupe-36-rgb) / <alpha-value>)", 900: "rgb(var(--taupe-25-rgb) / <alpha-value>)", 950: "rgb(var(--taupe-20-rgb) / <alpha-value>)"},
        indigo: {50: "rgb(var(--taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--taupe-26-rgb) / <alpha-value>)"},
        violet: {50: "rgb(var(--taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--taupe-26-rgb) / <alpha-value>)"},
        purple: {50: "rgb(var(--taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--taupe-26-rgb) / <alpha-value>)"},
        blue: {50: "rgb(var(--taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--taupe-26-rgb) / <alpha-value>)"},
        red: {50: "rgb(var(--taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--taupe-26-rgb) / <alpha-value>)"},
        rose: {50: "rgb(var(--taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--taupe-26-rgb) / <alpha-value>)"},
        pink: {50: "rgb(var(--taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--taupe-26-rgb) / <alpha-value>)"},
        fuchsia: {50: "rgb(var(--taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--taupe-26-rgb) / <alpha-value>)"},
        sky: {50: "rgb(var(--brass-93b-rgb) / <alpha-value>)", 100: "rgb(var(--brass-90b-rgb) / <alpha-value>)", 200: "rgb(var(--brass-84-rgb) / <alpha-value>)", 300: "rgb(var(--brass-78b-rgb) / <alpha-value>)", 400: "rgb(var(--brass-72-rgb) / <alpha-value>)", 500: "rgb(var(--brass-66-rgb) / <alpha-value>)", 600: "rgb(var(--brass-60-rgb) / <alpha-value>)", 700: "rgb(var(--brass-53-rgb) / <alpha-value>)", 800: "rgb(var(--brass-46-rgb) / <alpha-value>)", 900: "rgb(var(--brass-39-rgb) / <alpha-value>)", 950: "rgb(var(--brass-35-rgb) / <alpha-value>)"},
        cyan: {50: "rgb(var(--brass-93b-rgb) / <alpha-value>)", 100: "rgb(var(--brass-90b-rgb) / <alpha-value>)", 200: "rgb(var(--brass-84-rgb) / <alpha-value>)", 300: "rgb(var(--brass-78b-rgb) / <alpha-value>)", 400: "rgb(var(--brass-72-rgb) / <alpha-value>)", 500: "rgb(var(--brass-66-rgb) / <alpha-value>)", 600: "rgb(var(--brass-60-rgb) / <alpha-value>)", 700: "rgb(var(--brass-53-rgb) / <alpha-value>)", 800: "rgb(var(--brass-46-rgb) / <alpha-value>)", 900: "rgb(var(--brass-39-rgb) / <alpha-value>)", 950: "rgb(var(--brass-35-rgb) / <alpha-value>)"},
        emerald: {50: "rgb(var(--leaf-91-rgb) / <alpha-value>)", 100: "rgb(var(--leaf-87-rgb) / <alpha-value>)", 200: "rgb(var(--leaf-78-rgb) / <alpha-value>)", 300: "rgb(var(--leaf-69-rgb) / <alpha-value>)", 400: "rgb(var(--leaf-60-rgb) / <alpha-value>)", 500: "rgb(var(--leaf-52-rgb) / <alpha-value>)", 600: "rgb(var(--leaf-47-rgb) / <alpha-value>)", 700: "rgb(var(--leaf-43-rgb) / <alpha-value>)", 800: "rgb(var(--leaf-38-rgb) / <alpha-value>)", 900: "rgb(var(--leaf-32-rgb) / <alpha-value>)", 950: "rgb(var(--leaf-30-rgb) / <alpha-value>)"},
        green: {50: "rgb(var(--leaf-91-rgb) / <alpha-value>)", 100: "rgb(var(--leaf-87-rgb) / <alpha-value>)", 200: "rgb(var(--leaf-78-rgb) / <alpha-value>)", 300: "rgb(var(--leaf-69-rgb) / <alpha-value>)", 400: "rgb(var(--leaf-60-rgb) / <alpha-value>)", 500: "rgb(var(--leaf-52-rgb) / <alpha-value>)", 600: "rgb(var(--leaf-47-rgb) / <alpha-value>)", 700: "rgb(var(--leaf-43-rgb) / <alpha-value>)", 800: "rgb(var(--leaf-38-rgb) / <alpha-value>)", 900: "rgb(var(--leaf-32-rgb) / <alpha-value>)", 950: "rgb(var(--leaf-30-rgb) / <alpha-value>)"},
        teal: {50: "rgb(var(--leaf-91-rgb) / <alpha-value>)", 100: "rgb(var(--leaf-87-rgb) / <alpha-value>)", 200: "rgb(var(--leaf-78-rgb) / <alpha-value>)", 300: "rgb(var(--leaf-69-rgb) / <alpha-value>)", 400: "rgb(var(--leaf-60-rgb) / <alpha-value>)", 500: "rgb(var(--leaf-52-rgb) / <alpha-value>)", 600: "rgb(var(--leaf-47-rgb) / <alpha-value>)", 700: "rgb(var(--leaf-43-rgb) / <alpha-value>)", 800: "rgb(var(--leaf-38-rgb) / <alpha-value>)", 900: "rgb(var(--leaf-32-rgb) / <alpha-value>)", 950: "rgb(var(--leaf-30-rgb) / <alpha-value>)"},
        amber: {50: "rgb(var(--brass-93b-rgb) / <alpha-value>)", 100: "rgb(var(--brass-90b-rgb) / <alpha-value>)", 200: "rgb(var(--brass-84-rgb) / <alpha-value>)", 300: "rgb(var(--brass-78b-rgb) / <alpha-value>)", 400: "rgb(var(--brass-72-rgb) / <alpha-value>)", 500: "rgb(var(--brass-66-rgb) / <alpha-value>)", 600: "rgb(var(--brass-60-rgb) / <alpha-value>)", 700: "rgb(var(--brass-53-rgb) / <alpha-value>)", 800: "rgb(var(--brass-46-rgb) / <alpha-value>)", 900: "rgb(var(--brass-39-rgb) / <alpha-value>)", 950: "rgb(var(--brass-35-rgb) / <alpha-value>)"},
        yellow: {50: "rgb(var(--brass-93b-rgb) / <alpha-value>)", 100: "rgb(var(--brass-90b-rgb) / <alpha-value>)", 200: "rgb(var(--brass-84-rgb) / <alpha-value>)", 300: "rgb(var(--brass-78b-rgb) / <alpha-value>)", 400: "rgb(var(--brass-72-rgb) / <alpha-value>)", 500: "rgb(var(--brass-66-rgb) / <alpha-value>)", 600: "rgb(var(--brass-60-rgb) / <alpha-value>)", 700: "rgb(var(--brass-53-rgb) / <alpha-value>)", 800: "rgb(var(--brass-46-rgb) / <alpha-value>)", 900: "rgb(var(--brass-39-rgb) / <alpha-value>)", 950: "rgb(var(--brass-35-rgb) / <alpha-value>)"},
        orange: {50: "rgb(var(--brass-93b-rgb) / <alpha-value>)", 100: "rgb(var(--brass-90b-rgb) / <alpha-value>)", 200: "rgb(var(--brass-84-rgb) / <alpha-value>)", 300: "rgb(var(--brass-78b-rgb) / <alpha-value>)", 400: "rgb(var(--brass-72-rgb) / <alpha-value>)", 500: "rgb(var(--brass-66-rgb) / <alpha-value>)", 600: "rgb(var(--brass-60-rgb) / <alpha-value>)", 700: "rgb(var(--brass-53-rgb) / <alpha-value>)", 800: "rgb(var(--brass-46-rgb) / <alpha-value>)", 900: "rgb(var(--brass-39-rgb) / <alpha-value>)", 950: "rgb(var(--brass-35-rgb) / <alpha-value>)"},
        // Primary accent system
        violet: "rgb(var(--sindoor-57-rgb) / <alpha-value>)",
        "violet-2": "rgb(var(--sindoor-70-rgb) / <alpha-value>)",
        indigo: "rgb(var(--sindoor-55-rgb) / <alpha-value>)",
        sky: "rgb(var(--brass-74-rgb) / <alpha-value>)",
        cyan: "rgb(var(--brass-78-rgb) / <alpha-value>)",
        lime: "rgb(var(--leaf-82-rgb) / <alpha-value>)",
        mint: "rgb(var(--leaf-75-rgb) / <alpha-value>)",
        steel: "rgb(var(--taupe-71-rgb) / <alpha-value>)",
        // legacy aliases (kept so previously-used utility classes still resolve)
        fuchsia: "rgb(var(--sindoor-55-rgb) / <alpha-value>)",
        pink: "rgb(var(--brass-74-rgb) / <alpha-value>)",
        ember: "rgb(var(--taupe-71-rgb) / <alpha-value>)"
      },
      // ink-textColor:start — generated by tools/apply-ink.py; text uses ink, fills keep the brand colour
      textColor: {
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
        slate: {50: "rgb(var(--ink-taupe-94d-rgb) / <alpha-value>)", 100: "rgb(var(--ink-taupe-91c-rgb) / <alpha-value>)", 200: "rgb(var(--ink-taupe-85-rgb) / <alpha-value>)", 300: "rgb(var(--ink-taupe-78-rgb) / <alpha-value>)", 400: "rgb(var(--ink-taupe-72-rgb) / <alpha-value>)", 500: "rgb(var(--ink-taupe-64-rgb) / <alpha-value>)", 600: "rgb(var(--ink-taupe-55-rgb) / <alpha-value>)", 700: "rgb(var(--ink-taupe-46-rgb) / <alpha-value>)", 800: "rgb(var(--ink-taupe-36-rgb) / <alpha-value>)", 900: "rgb(var(--ink-taupe-25-rgb) / <alpha-value>)", 950: "rgb(var(--ink-taupe-20-rgb) / <alpha-value>)"},
        gray: {50: "rgb(var(--ink-taupe-94d-rgb) / <alpha-value>)", 100: "rgb(var(--ink-taupe-91c-rgb) / <alpha-value>)", 200: "rgb(var(--ink-taupe-85-rgb) / <alpha-value>)", 300: "rgb(var(--ink-taupe-78-rgb) / <alpha-value>)", 400: "rgb(var(--ink-taupe-72-rgb) / <alpha-value>)", 500: "rgb(var(--ink-taupe-64-rgb) / <alpha-value>)", 600: "rgb(var(--ink-taupe-55-rgb) / <alpha-value>)", 700: "rgb(var(--ink-taupe-46-rgb) / <alpha-value>)", 800: "rgb(var(--ink-taupe-36-rgb) / <alpha-value>)", 900: "rgb(var(--ink-taupe-25-rgb) / <alpha-value>)", 950: "rgb(var(--ink-taupe-20-rgb) / <alpha-value>)"},
        zinc: {50: "rgb(var(--ink-taupe-94d-rgb) / <alpha-value>)", 100: "rgb(var(--ink-taupe-91c-rgb) / <alpha-value>)", 200: "rgb(var(--ink-taupe-85-rgb) / <alpha-value>)", 300: "rgb(var(--ink-taupe-78-rgb) / <alpha-value>)", 400: "rgb(var(--ink-taupe-72-rgb) / <alpha-value>)", 500: "rgb(var(--ink-taupe-64-rgb) / <alpha-value>)", 600: "rgb(var(--ink-taupe-55-rgb) / <alpha-value>)", 700: "rgb(var(--ink-taupe-46-rgb) / <alpha-value>)", 800: "rgb(var(--ink-taupe-36-rgb) / <alpha-value>)", 900: "rgb(var(--ink-taupe-25-rgb) / <alpha-value>)", 950: "rgb(var(--ink-taupe-20-rgb) / <alpha-value>)"},
        neutral: {50: "rgb(var(--ink-taupe-94d-rgb) / <alpha-value>)", 100: "rgb(var(--ink-taupe-91c-rgb) / <alpha-value>)", 200: "rgb(var(--ink-taupe-85-rgb) / <alpha-value>)", 300: "rgb(var(--ink-taupe-78-rgb) / <alpha-value>)", 400: "rgb(var(--ink-taupe-72-rgb) / <alpha-value>)", 500: "rgb(var(--ink-taupe-64-rgb) / <alpha-value>)", 600: "rgb(var(--ink-taupe-55-rgb) / <alpha-value>)", 700: "rgb(var(--ink-taupe-46-rgb) / <alpha-value>)", 800: "rgb(var(--ink-taupe-36-rgb) / <alpha-value>)", 900: "rgb(var(--ink-taupe-25-rgb) / <alpha-value>)", 950: "rgb(var(--ink-taupe-20-rgb) / <alpha-value>)"},
        stone: {50: "rgb(var(--ink-taupe-94d-rgb) / <alpha-value>)", 100: "rgb(var(--ink-taupe-91c-rgb) / <alpha-value>)", 200: "rgb(var(--ink-taupe-85-rgb) / <alpha-value>)", 300: "rgb(var(--ink-taupe-78-rgb) / <alpha-value>)", 400: "rgb(var(--ink-taupe-72-rgb) / <alpha-value>)", 500: "rgb(var(--ink-taupe-64-rgb) / <alpha-value>)", 600: "rgb(var(--ink-taupe-55-rgb) / <alpha-value>)", 700: "rgb(var(--ink-taupe-46-rgb) / <alpha-value>)", 800: "rgb(var(--ink-taupe-36-rgb) / <alpha-value>)", 900: "rgb(var(--ink-taupe-25-rgb) / <alpha-value>)", 950: "rgb(var(--ink-taupe-20-rgb) / <alpha-value>)"},
        indigo: {50: "rgb(var(--ink-taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--ink-taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--ink-taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--ink-sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--ink-sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--ink-sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--ink-sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--ink-sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--ink-sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--ink-taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--ink-taupe-26-rgb) / <alpha-value>)"},
        violet: {50: "rgb(var(--ink-taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--ink-taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--ink-taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--ink-sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--ink-sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--ink-sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--ink-sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--ink-sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--ink-sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--ink-taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--ink-taupe-26-rgb) / <alpha-value>)"},
        purple: {50: "rgb(var(--ink-taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--ink-taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--ink-taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--ink-sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--ink-sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--ink-sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--ink-sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--ink-sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--ink-sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--ink-taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--ink-taupe-26-rgb) / <alpha-value>)"},
        blue: {50: "rgb(var(--ink-taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--ink-taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--ink-taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--ink-sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--ink-sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--ink-sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--ink-sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--ink-sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--ink-sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--ink-taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--ink-taupe-26-rgb) / <alpha-value>)"},
        red: {50: "rgb(var(--ink-taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--ink-taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--ink-taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--ink-sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--ink-sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--ink-sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--ink-sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--ink-sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--ink-sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--ink-taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--ink-taupe-26-rgb) / <alpha-value>)"},
        rose: {50: "rgb(var(--ink-taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--ink-taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--ink-taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--ink-sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--ink-sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--ink-sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--ink-sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--ink-sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--ink-sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--ink-taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--ink-taupe-26-rgb) / <alpha-value>)"},
        pink: {50: "rgb(var(--ink-taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--ink-taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--ink-taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--ink-sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--ink-sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--ink-sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--ink-sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--ink-sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--ink-sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--ink-taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--ink-taupe-26-rgb) / <alpha-value>)"},
        fuchsia: {50: "rgb(var(--ink-taupe-91d-rgb) / <alpha-value>)", 100: "rgb(var(--ink-taupe-86b-rgb) / <alpha-value>)", 200: "rgb(var(--ink-taupe-77-rgb) / <alpha-value>)", 300: "rgb(var(--ink-sindoor-68-rgb) / <alpha-value>)", 400: "rgb(var(--ink-sindoor-61b-rgb) / <alpha-value>)", 500: "rgb(var(--ink-sindoor-55b-rgb) / <alpha-value>)", 600: "rgb(var(--ink-sindoor-49b-rgb) / <alpha-value>)", 700: "rgb(var(--ink-sindoor-43-rgb) / <alpha-value>)", 800: "rgb(var(--ink-sindoor-36-rgb) / <alpha-value>)", 900: "rgb(var(--ink-taupe-29-rgb) / <alpha-value>)", 950: "rgb(var(--ink-taupe-26-rgb) / <alpha-value>)"},
        sky: {50: "rgb(var(--ink-brass-93b-rgb) / <alpha-value>)", 100: "rgb(var(--ink-brass-90b-rgb) / <alpha-value>)", 200: "rgb(var(--ink-brass-84-rgb) / <alpha-value>)", 300: "rgb(var(--ink-brass-78b-rgb) / <alpha-value>)", 400: "rgb(var(--ink-brass-72-rgb) / <alpha-value>)", 500: "rgb(var(--ink-brass-66-rgb) / <alpha-value>)", 600: "rgb(var(--ink-brass-60-rgb) / <alpha-value>)", 700: "rgb(var(--ink-brass-53-rgb) / <alpha-value>)", 800: "rgb(var(--ink-brass-46-rgb) / <alpha-value>)", 900: "rgb(var(--ink-brass-39-rgb) / <alpha-value>)", 950: "rgb(var(--ink-brass-35-rgb) / <alpha-value>)"},
        cyan: {50: "rgb(var(--ink-brass-93b-rgb) / <alpha-value>)", 100: "rgb(var(--ink-brass-90b-rgb) / <alpha-value>)", 200: "rgb(var(--ink-brass-84-rgb) / <alpha-value>)", 300: "rgb(var(--ink-brass-78b-rgb) / <alpha-value>)", 400: "rgb(var(--ink-brass-72-rgb) / <alpha-value>)", 500: "rgb(var(--ink-brass-66-rgb) / <alpha-value>)", 600: "rgb(var(--ink-brass-60-rgb) / <alpha-value>)", 700: "rgb(var(--ink-brass-53-rgb) / <alpha-value>)", 800: "rgb(var(--ink-brass-46-rgb) / <alpha-value>)", 900: "rgb(var(--ink-brass-39-rgb) / <alpha-value>)", 950: "rgb(var(--ink-brass-35-rgb) / <alpha-value>)"},
        emerald: {50: "rgb(var(--ink-leaf-91-rgb) / <alpha-value>)", 100: "rgb(var(--ink-leaf-87-rgb) / <alpha-value>)", 200: "rgb(var(--ink-leaf-78-rgb) / <alpha-value>)", 300: "rgb(var(--ink-leaf-69-rgb) / <alpha-value>)", 400: "rgb(var(--ink-leaf-60-rgb) / <alpha-value>)", 500: "rgb(var(--ink-leaf-52-rgb) / <alpha-value>)", 600: "rgb(var(--ink-leaf-47-rgb) / <alpha-value>)", 700: "rgb(var(--ink-leaf-43-rgb) / <alpha-value>)", 800: "rgb(var(--ink-leaf-38-rgb) / <alpha-value>)", 900: "rgb(var(--ink-leaf-32-rgb) / <alpha-value>)", 950: "rgb(var(--ink-leaf-30-rgb) / <alpha-value>)"},
        green: {50: "rgb(var(--ink-leaf-91-rgb) / <alpha-value>)", 100: "rgb(var(--ink-leaf-87-rgb) / <alpha-value>)", 200: "rgb(var(--ink-leaf-78-rgb) / <alpha-value>)", 300: "rgb(var(--ink-leaf-69-rgb) / <alpha-value>)", 400: "rgb(var(--ink-leaf-60-rgb) / <alpha-value>)", 500: "rgb(var(--ink-leaf-52-rgb) / <alpha-value>)", 600: "rgb(var(--ink-leaf-47-rgb) / <alpha-value>)", 700: "rgb(var(--ink-leaf-43-rgb) / <alpha-value>)", 800: "rgb(var(--ink-leaf-38-rgb) / <alpha-value>)", 900: "rgb(var(--ink-leaf-32-rgb) / <alpha-value>)", 950: "rgb(var(--ink-leaf-30-rgb) / <alpha-value>)"},
        teal: {50: "rgb(var(--ink-leaf-91-rgb) / <alpha-value>)", 100: "rgb(var(--ink-leaf-87-rgb) / <alpha-value>)", 200: "rgb(var(--ink-leaf-78-rgb) / <alpha-value>)", 300: "rgb(var(--ink-leaf-69-rgb) / <alpha-value>)", 400: "rgb(var(--ink-leaf-60-rgb) / <alpha-value>)", 500: "rgb(var(--ink-leaf-52-rgb) / <alpha-value>)", 600: "rgb(var(--ink-leaf-47-rgb) / <alpha-value>)", 700: "rgb(var(--ink-leaf-43-rgb) / <alpha-value>)", 800: "rgb(var(--ink-leaf-38-rgb) / <alpha-value>)", 900: "rgb(var(--ink-leaf-32-rgb) / <alpha-value>)", 950: "rgb(var(--ink-leaf-30-rgb) / <alpha-value>)"},
        amber: {50: "rgb(var(--ink-brass-93b-rgb) / <alpha-value>)", 100: "rgb(var(--ink-brass-90b-rgb) / <alpha-value>)", 200: "rgb(var(--ink-brass-84-rgb) / <alpha-value>)", 300: "rgb(var(--ink-brass-78b-rgb) / <alpha-value>)", 400: "rgb(var(--ink-brass-72-rgb) / <alpha-value>)", 500: "rgb(var(--ink-brass-66-rgb) / <alpha-value>)", 600: "rgb(var(--ink-brass-60-rgb) / <alpha-value>)", 700: "rgb(var(--ink-brass-53-rgb) / <alpha-value>)", 800: "rgb(var(--ink-brass-46-rgb) / <alpha-value>)", 900: "rgb(var(--ink-brass-39-rgb) / <alpha-value>)", 950: "rgb(var(--ink-brass-35-rgb) / <alpha-value>)"},
        yellow: {50: "rgb(var(--ink-brass-93b-rgb) / <alpha-value>)", 100: "rgb(var(--ink-brass-90b-rgb) / <alpha-value>)", 200: "rgb(var(--ink-brass-84-rgb) / <alpha-value>)", 300: "rgb(var(--ink-brass-78b-rgb) / <alpha-value>)", 400: "rgb(var(--ink-brass-72-rgb) / <alpha-value>)", 500: "rgb(var(--ink-brass-66-rgb) / <alpha-value>)", 600: "rgb(var(--ink-brass-60-rgb) / <alpha-value>)", 700: "rgb(var(--ink-brass-53-rgb) / <alpha-value>)", 800: "rgb(var(--ink-brass-46-rgb) / <alpha-value>)", 900: "rgb(var(--ink-brass-39-rgb) / <alpha-value>)", 950: "rgb(var(--ink-brass-35-rgb) / <alpha-value>)"},
        orange: {50: "rgb(var(--ink-brass-93b-rgb) / <alpha-value>)", 100: "rgb(var(--ink-brass-90b-rgb) / <alpha-value>)", 200: "rgb(var(--ink-brass-84-rgb) / <alpha-value>)", 300: "rgb(var(--ink-brass-78b-rgb) / <alpha-value>)", 400: "rgb(var(--ink-brass-72-rgb) / <alpha-value>)", 500: "rgb(var(--ink-brass-66-rgb) / <alpha-value>)", 600: "rgb(var(--ink-brass-60-rgb) / <alpha-value>)", 700: "rgb(var(--ink-brass-53-rgb) / <alpha-value>)", 800: "rgb(var(--ink-brass-46-rgb) / <alpha-value>)", 900: "rgb(var(--ink-brass-39-rgb) / <alpha-value>)", 950: "rgb(var(--ink-brass-35-rgb) / <alpha-value>)"},
        // Primary accent system
        violet: "rgb(var(--ink-sindoor-57-rgb) / <alpha-value>)",
        "violet-2": "rgb(var(--ink-sindoor-70-rgb) / <alpha-value>)",
        indigo: "rgb(var(--ink-sindoor-55-rgb) / <alpha-value>)",
        sky: "rgb(var(--ink-brass-74-rgb) / <alpha-value>)",
        cyan: "rgb(var(--ink-brass-78-rgb) / <alpha-value>)",
        lime: "rgb(var(--ink-leaf-82-rgb) / <alpha-value>)",
        mint: "rgb(var(--ink-leaf-75-rgb) / <alpha-value>)",
        steel: "rgb(var(--ink-taupe-71-rgb) / <alpha-value>)",
        // legacy aliases (kept so previously-used utility classes still resolve)
        fuchsia: "rgb(var(--ink-sindoor-55-rgb) / <alpha-value>)",
        pink: "rgb(var(--ink-brass-74-rgb) / <alpha-value>)",
        ember: "rgb(var(--ink-taupe-71-rgb) / <alpha-value>)"
      },
      // ink-textColor:end
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
        glow: "0 0 60px -10px rgb(var(--sindoor-57-rgb) / 0.45), 0 0 100px -20px rgb(var(--brass-68-rgb) / 0.25)",
        "glow-sm": "0 0 24px -4px rgb(var(--sindoor-57-rgb) / 0.4)",
        card: "0 1px 0 0 rgba(255,255,255,0.04), 0 24px 60px -30px rgba(0,0,0,0.6)",
        inset: "inset 0 1px 0 0 rgba(255,255,255,0.06)"
      },
      backgroundImage: {
        "grid-dots":
          "radial-gradient(rgba(255,255,255,0.06) 1px, transparent 1px)",
        aurora:
          "conic-gradient(from 180deg at 50% 50%, var(--sindoor-57) 0deg, var(--sindoor-55) 90deg, var(--brass-78) 200deg, var(--brass-74) 300deg, var(--sindoor-57) 360deg)"
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
