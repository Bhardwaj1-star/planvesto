import fs from "fs";
import path from "path";

const WEBSITE_DIR = "C:\\Users\\lenovo\\Desktop\\website";
const APP_DIR = path.join(process.cwd(), "app");

const ROUTES = [
  { file: "plan.html", route: "plan", component: "PlanPage", hasNav: true },
  { file: "invest.html", route: "invest", component: "InvestPage", hasNav: true },
  { file: "protect.html", route: "protect", component: "ProtectPage", hasNav: true },
  { file: "decide.html", route: "decide", component: "DecidePage", hasNav: true },
  { file: "learn.html", route: "learn", component: "LearnPage", hasNav: true, hasSearch: true },
  { file: "about.html", route: "about", component: "AboutPage", hasNav: true },
  { file: "contact.html", route: "contact", component: "ContactPage", hasNav: true, hasContactForm: true },
  { file: "login.html", route: "login", component: "LoginPage", hasNav: false, hasLoginForm: true },
  { file: "signup.html", route: "signup", component: "SignupPage", hasNav: false, hasSignupForm: true },
  { file: "privacy.html", route: "privacy", component: "PrivacyPage", hasNav: true },
  { file: "terms.html", route: "terms", component: "TermsPage", hasNav: true },
  { file: "disclaimer.html", route: "disclaimer", component: "DisclaimerPage", hasNav: true },
];

const LINK_MAP = {
  "index.html": "/",
  "home.html": "/",
  "plan.html": "/plan",
  "invest.html": "/invest",
  "protect.html": "/protect",
  "decide.html": "/decide",
  "learn.html": "/learn",
  "about.html": "/about",
  "contact.html": "/contact",
  "login.html": "/login",
  "signup.html": "/signup",
  "privacy.html": "/privacy",
  "terms.html": "/terms",
  "disclaimer.html": "/disclaimer",
};

function extractBody(html) {
  const bodyMatch = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  if (!bodyMatch) throw new Error("No body found");
  let body = bodyMatch[1];
  body = body.replace(/<script[\s\S]*?<\/script>/gi, "");
  return body.trim();
}

function extractStyles(html) {
  const styles = [];
  const re = /<style[^>]*>([\s\S]*?)<\/style>/gi;
  let m;
  while ((m = re.exec(html))) styles.push(m[1].trim());
  return styles.join("\n\n");
}

function replaceLinks(html) {
  let out = html;
  for (const [from, to] of Object.entries(LINK_MAP)) {
    const hashRe = new RegExp(`href=["']${from.replace(".", "\\.")}(#[^"']*)["']`, "gi");
    out = out.replace(hashRe, (_, hash) => `href="${to}${hash}"`);
    const plainRe = new RegExp(`href=["']${from.replace(".", "\\.")}["']`, "gi");
    out = out.replace(plainRe, `href="${to}"`);
  }
  return out;
}

function htmlToJsx(html) {
  let jsx = html;
  jsx = jsx.replace(/<!--[\s\S]*?-->/g, "");
  jsx = jsx.replace(/\bclass=/g, "className=");
  jsx = jsx.replace(/\bfor=/g, "htmlFor=");
  jsx = jsx.replace(/\bstroke-width=/g, "strokeWidth=");
  jsx = jsx.replace(/\bstroke-linecap=/g, "strokeLinecap=");
  jsx = jsx.replace(/\bstroke-linejoin=/g, "strokeLinejoin=");
  jsx = jsx.replace(/\bfill-rule=/g, "fillRule=");
  jsx = jsx.replace(/\bclip-rule=/g, "clipRule=");
  jsx = jsx.replace(/\btabindex=/g, "tabIndex=");
  jsx = jsx.replace(/\breadonly\b/g, "readOnly");
  jsx = jsx.replace(/\bmaxlength=/g, "maxLength=");
  jsx = jsx.replace(/\bminlength=/g, "minLength=");
  jsx = jsx.replace(/\bcolspan=/g, "colSpan=");
  jsx = jsx.replace(/\browspan=/g, "rowSpan=");
  jsx = jsx.replace(/\bcrossorigin\b/g, "crossOrigin");
  jsx = jsx.replace(/\bviewbox=/gi, "viewBox=");
  jsx = jsx.replace(/\bautocomplete=/g, "autoComplete=");
  jsx = jsx.replace(/\bautofocus\b/g, "autoFocus");
  jsx = jsx.replace(/\benctype=/g, "encType=");
  jsx = jsx.replace(/\bnovalidate\b/g, "noValidate");

  jsx = jsx.replace(/<(\w+)([^>]*?)\s*\/>/g, "<$1$2 />");
  const voidTags = ["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"];
  for (const tag of voidTags) {
    const re = new RegExp(`<${tag}([^>/]*)(?<!/)>`, "gi");
    jsx = jsx.replace(re, `<${tag}$1 />`);
  }

  jsx = jsx.replace(/Terms & Conditions/g, "Terms &amp; Conditions");
  jsx = jsx.replace(/<span id="currentYear"><\/span>/g, '<span id="currentYear">{new Date().getFullYear()}</span>');

  jsx = jsx.replace(/\brows="(\d+)"/g, 'rows={$1}');
  jsx = jsx.replace(/\bcols="(\d+)"/g, 'cols={$1}');
  jsx = jsx.replace(/\bmaxLength="(\d+)"/g, 'maxLength={$1}');
  jsx = jsx.replace(/\bminLength="(\d+)"/g, 'minLength={$1}');
  jsx = jsx.replace(/\btabIndex="(\d+)"/g, 'tabIndex={$1}');

  return jsx;
}

function insertHomeNav(jsx, activeRoute) {
  const homeActive = activeRoute === "home";
  const homeClass = homeActive
    ? "text-sm font-bold text-navy-900"
    : "text-sm font-medium text-slate-600 transition hover:text-navy-900";
  const homeLink = `<a className="${homeClass}" href="/">\n                Home\n            </a>\n\n            `;

  if (!jsx.includes('aria-label="Main navigation"') && !jsx.includes("aria-label=\"Main navigation\"")) {
    return jsx;
  }

  return jsx.replace(
    /(<nav[^>]*aria-label="Main navigation"[^>]*>\s*)/i,
    `$1${homeLink}`
  );
}

function patchMobileMenu(jsx) {
  jsx = jsx.replace(/aria-expanded="false"/g, "aria-expanded={menuOpen}");
  jsx = jsx.replace(
    /id="menuButton"([^>]*?)type="button"/,
    'id="menuButton"$1type="button" onClick={() => setMenuOpen(!menuOpen)}'
  );
  jsx = jsx.replace(
    /id="mobileMenu"\s+className="mobile-menu[^"]*"/,
    'id="mobileMenu" className={`mobile-menu border-t border-slate-200 bg-white lg:hidden ${menuOpen ? "" : "hidden"}`}'
  );
  return jsx;
}

function getImports(config) {
  const hooks = ["useState"];
  const imports = [`import { ${hooks.join(", ")} } from "react";`];
  if (config.hasNav) imports.push('import { useMobileMenuClose } from "../../hooks/useMobileMenuClose";');
  if (config.hasSearch) imports.push('import { useArticleSearch } from "../../hooks/useArticleSearch";');
  if (config.hasContactForm) imports.push('import { useContactForm } from "../../hooks/useContactForm";');
  if (config.hasLoginForm) imports.push('import { useLoginForm } from "../../hooks/useLoginForm";');
  if (config.hasSignupForm) imports.push('import { useSignupForm } from "../../hooks/useSignupForm";');
  return imports.join("\n");
}

function getEffects(config) {
  const effects = [];
  if (config.hasNav) effects.push("  useMobileMenuClose(setMenuOpen);");
  if (config.hasSearch) effects.push("  useArticleSearch();");
  if (config.hasContactForm) effects.push("  useContactForm();");
  if (config.hasLoginForm) effects.push("  useLoginForm();");
  if (config.hasSignupForm) effects.push("  useSignupForm();");
  return effects.length ? "\n" + effects.join("\n") + "\n" : "";
}

function generatePage(config, jsx) {
  const stateLine = config.hasNav ? "  const [menuOpen, setMenuOpen] = useState(false);\n" : "";
  const effects = getEffects(config);
  return `"use client";

${getImports(config)}

export default function ${config.component}() {
${stateLine}${effects}
  return (
    <>
${jsx}
    </>
  );
}
`;
}

const allStyles = new Set();

for (const config of ROUTES) {
  const htmlPath = path.join(WEBSITE_DIR, config.file);
  const html = fs.readFileSync(htmlPath, "utf8");
  extractStyles(html)
    .split("\n")
    .filter((l) => l.trim().startsWith("."))
    .forEach((l) => allStyles.add(l));

  let body = extractBody(html);
  body = replaceLinks(body);
  body = insertHomeNav(body, config.route);
  let jsx = htmlToJsx(body);
  if (config.hasNav) jsx = patchMobileMenu(jsx);

  const pageContent = generatePage(config, jsx);
  const outDir = path.join(APP_DIR, config.route);
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, "page.tsx"), pageContent);
  console.log(`Wrote ${config.route}/page.tsx`);
}

const globalsPath = path.join(APP_DIR, "globals.css");
let globals = fs.readFileSync(globalsPath, "utf8");

const extraCss = `
/* Page-specific styles consolidated from original HTML */
.step-line {
  position: relative;
}

.step-line::after {
  content: "";
  position: absolute;
  left: 20px;
  top: 45px;
  bottom: -30px;
  width: 1px;
  background: #CBD5E1;
}

.step-line:last-child::after {
  display: none;
}

.decision-line::after {
  content: "";
  position: absolute;
  left: 23px;
  top: 48px;
  bottom: -28px;
  width: 1px;
  background: #CBD5E1;
}

.decision-line:last-child::after {
  display: none;
}

.risk-line {
  position: relative;
}

.risk-line::after {
  content: "";
  position: absolute;
  left: 20px;
  top: 45px;
  bottom: -30px;
  width: 1px;
  background: #CBD5E1;
}

.risk-line:last-child::after {
  display: none;
}

.allocation-bar {
  transition: width 0.8s ease;
}

.value-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.value-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 18px 45px rgba(11, 31, 51, 0.08);
  border-color: #CBD5E1;
}

.article-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.article-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 18px 45px rgba(11, 31, 51, 0.08);
  border-color: #CBD5E1;
}

.contact-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.contact-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 18px 45px rgba(11, 31, 51, 0.08);
  border-color: #CBD5E1;
}

.form-field {
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-field:focus {
  border-color: #14B8A6;
  box-shadow: 0 0 0 4px rgba(20, 184, 166, 0.10);
  outline: none;
}

.login-grid,
.signup-grid {
  background-image:
    linear-gradient(rgba(11, 31, 51, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(11, 31, 51, 0.04) 1px, transparent 1px);
  background-size: 44px 44px;
}

.password-toggle {
  transition: color 0.2s ease;
}

.password-toggle:hover {
  color: #0B1F33;
}

.login-card,
.signup-card {
  animation: cardIn 0.35s ease-out;
}

@keyframes cardIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.password-strength-bar {
  transition: width 0.25s ease, background-color 0.25s ease;
}
`;

if (!globals.includes(".step-line")) {
  globals = globals.replace(/@tailwind utilities;\n/, `@tailwind utilities;\n${extraCss}\n`);
  fs.writeFileSync(globalsPath, globals);
  console.log("Updated globals.css");
}

console.log("Migration complete.");
