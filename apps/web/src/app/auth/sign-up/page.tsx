"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";

import { useAuth } from "@/components/auth-provider";
import { PasswordInput } from "@/components/password-input";
import { useToast } from "@/components/toaster";

const apiBase = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function SignUpPage() {
  const router = useRouter();
  const showToast = useToast();
  const { refresh } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch(`${apiBase}/auth/register`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, email, password, confirm_password: confirmPassword }),
      });

      const payload = (await response.json().catch(() => null)) as { detail?: string } | null;
      if (!response.ok) {
        const message = payload?.detail || "We couldn't create your account. Please try again.";
        throw new Error(message);
      }

      await refresh();

      showToast({
        title: "Account created successfully",
        description: "Welcome to GP Autos.",
        variant: "success",
      });

      router.push("/");
    } catch (submitError) {
      const message =
        submitError instanceof Error && submitError.message && !submitError.message.includes("Failed to fetch")
          ? submitError.message
          : "Unable to connect to GP Autos. Please check your connection and try again.";
      setError(message);
      showToast({
        title: "Sign up failed",
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

            <form onSubmit={handleSubmit}>
              <div className="auth-field">
                <label htmlFor="signup-name">Full name</label>
                <input
                  id="signup-name"
                  type="text"
                  name="name"
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  autoComplete="name"
                  required
                />
              </div>

              <div className="auth-field">
                <label htmlFor="signup-email">Email address</label>
                <input
                  id="signup-email"
                  type="email"
                  name="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  autoComplete="email"
                  required
                />
              </div>

              <PasswordInput
                id="signup-password"
                label="Password"
                name="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                autoComplete="new-password"
                minLength={8}
                required
              />

              <PasswordInput
                id="signup-confirm-password"
                label="Confirm password"
                name="confirmPassword"
                value={confirmPassword}
                onChange={(event) => setConfirmPassword(event.target.value)}
                autoComplete="new-password"
                minLength={8}
                required
              />

              {error ? (
                <p aria-live="polite" style={{ color: "#fda4af", marginTop: "1rem" }}>
                  {error}
                </p>
              ) : null}

              <button className="button button-cyan" type="submit" disabled={isSubmitting}>
                {isSubmitting ? "Creating account..." : "Create account"}
              </button>
            </form>

            <div className="auth-divider">or continue with</div>

            <a className="button button-dark" href={`${apiBase}/auth/google`}>
              Continue with Google <span aria-hidden="true">↗</span>
            </a>

            <p className="auth-cta-copy" style={{ marginTop: "1rem" }}>Already have an account?</p>
            <Link className="button button-dark" href="/auth/sign-in">Sign in</Link>

            <p className="auth-footer">
              By continuing, you agree to create a secure GP Autos account. <Link href="/vehicles">Browse inventory</Link>
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
