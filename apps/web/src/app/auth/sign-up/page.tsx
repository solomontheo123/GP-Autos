import Link from "next/link";
import { SiteHeader } from "@/components/site-header";

const apiBase = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function SignUpPage() {
  return (
    <main>
      <SiteHeader />
      <section className="auth-shell">
        <aside className="auth-brand" aria-label="GP Autos brand panel">
          <div className="auth-brand-content">
            <p className="eyebrow">A better way to shop</p>
            <h1>Your next car should feel effortless.</h1>
            <p>Save your favourites, track your order, and move from curiosity to ownership with a single trusted account.</p>
          </div>
        </aside>

        <div className="auth-panel">
          <div className="auth-card">
            <p className="eyebrow">Create account</p>
            <h1>Find the right fit faster.</h1>
            <p>Get a personalized GP Autos experience with secure access, recent order tracking, and a smoother checkout flow.</p>

            <a className="button button-cyan" href={`${apiBase}/auth/google`}>
              Continue with Google <span aria-hidden="true">↗</span>
            </a>

            <div className="auth-divider">already a member</div>

            <p className="auth-cta-copy">Already have an account?</p>
            <Link className="button button-dark" href="/auth/sign-in">Sign in</Link>

            <p className="auth-footer">
              By continuing, you agree to use your Google account to create a GP Autos profile. <Link href="/vehicles">Browse inventory</Link>
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
