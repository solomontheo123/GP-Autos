"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";

import { useToast } from "@/components/toaster";

const apiBase = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function SignInPage() {
  const router = useRouter();
  const showToast = useToast();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      const response = await fetch(`${apiBase}/auth/login`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const payload = (await response.json().catch(() => null)) as { detail?: string } | null;
      if (!response.ok) {
        const message = payload?.detail || "Invalid email or password.";
        throw new Error(message);
      }

      showToast({
        title: "Signed in",
        description: "Welcome back to GP Autos.",
        variant: "success",
      });

      router.push("/");
      router.refresh();
    } catch (submitError) {
      const message =
        submitError instanceof Error && submitError.message && !submitError.message.includes("Failed to fetch")
          ? submitError.message
          : "Unable to connect to GP Autos. Please check your connection and try again.";
      setError(message);
      showToast({
        title: "Sign in failed",
        description: message,
        variant: "error",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main>
      <section className="auth-shell">
        <aside className="auth-brand" aria-label="GP Autos brand panel">
          <div className="auth-brand-content">
            <Link href="/" className="auth-brand-home">← Back to GP Autos</Link>
            <p className="eyebrow">Built for better buying</p>
            <h1>Drive your next decision with confidence.</h1>
            <p>Manage your saved cars, recent purchases, and all the details that matter before you commit.</p>
          </div>
        </aside>

        <div className="auth-panel">
          <div className="auth-card">
            <p className="eyebrow">Welcome back</p>
            <h1>Good to have you here.</h1>
            <p>Sign in securely to continue checkout, review your orders, and keep your GP Autos experience in sync.</p>

            <form onSubmit={handleSubmit}>
              <div className="auth-field">
                <label htmlFor="signin-email">Email address</label>
                <input
                  id="signin-email"
                  type="email"
                  name="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  autoComplete="email"
                  required
                />
              </div>

              <div className="auth-field">
                <label htmlFor="signin-password">Password</label>
                <input
                  id="signin-password"
                  type="password"
                  name="password"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  autoComplete="current-password"
                  required
                />
              </div>

              {error ? (
                <p aria-live="polite" style={{ color: "#fda4af", marginTop: "1rem" }}>
                  {error}
                </p>
              ) : null}

              <button className="button button-cyan" type="submit" disabled={isSubmitting}>
                {isSubmitting ? "Signing in..." : "Sign in"}
              </button>
            </form>

            <div className="auth-divider">or continue with</div>

            <a className="button button-dark" href={`${apiBase}/auth/google`}>
              Continue with Google <span aria-hidden="true">↗</span>
            </a>

            <p className="auth-cta-copy" style={{ marginTop: "1rem" }}>Don&apos;t have an account?</p>
            <Link className="button button-dark" href="/auth/sign-up">Create an account</Link>

            <p className="auth-footer">
              Need a quick refresher? <Link href="/vehicles">View available vehicles</Link>
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
