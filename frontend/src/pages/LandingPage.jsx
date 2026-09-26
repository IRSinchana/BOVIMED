import { Link } from 'react-router-dom'
import { Camera, ScanLine, ShieldCheck } from 'lucide-react'
import { BrandMark } from '../components/AiModeBadge'
import { DISCLAIMER } from '../utils/analysis'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-cream text-forest">
      <header className="mx-auto flex max-w-6xl items-center justify-between px-4 py-5 sm:px-6">
        <BrandMark />
        <Link
          to="/app"
          className="rounded-xl border border-earth bg-white px-4 py-2 text-sm font-semibold text-forest"
        >
          Open App
        </Link>
      </header>

      <section className="relative overflow-hidden">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_top,_rgba(64,145,108,0.18),_transparent_55%)]" />
        <div className="relative mx-auto grid max-w-6xl gap-10 px-4 py-16 sm:px-6 lg:grid-cols-2 lg:items-center lg:py-24">
          <div>
            <p className="font-display text-sm font-semibold tracking-[0.18em] text-fresh uppercase">
              BOVIMED
            </p>
            <h1 className="mt-3 font-display text-4xl font-bold tracking-tight text-forest sm:text-5xl">
              Smart Vision for Healthier Herds
            </h1>
            <p className="mt-4 max-w-xl text-lg leading-relaxed text-forest/75">
              Detect potential mastitis early with AI-powered cow health analysis.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                to="/app/analyze"
                className="inline-flex items-center gap-2 rounded-2xl bg-forest px-6 py-3.5 text-base font-semibold text-cream shadow-sm"
              >
                <ScanLine className="h-5 w-5" />
                Analyze Cow Image
              </Link>
              <Link
                to="/app/camera"
                className="inline-flex items-center gap-2 rounded-2xl border border-forest/20 bg-white px-6 py-3.5 text-base font-semibold text-forest"
              >
                <Camera className="h-5 w-5" />
                Scan with Camera
              </Link>
            </div>
            <p className="mt-6 flex items-start gap-2 text-sm text-forest/60">
              <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-fresh" />
              AI-assisted screening — not a veterinary diagnosis.
            </p>
          </div>
          <div className="rounded-[2rem] border border-earth bg-gradient-to-br from-forest to-fresh p-8 text-cream shadow-lg">
            <p className="font-display text-sm font-semibold tracking-wide uppercase opacity-80">
              How it works
            </p>
            <ol className="mt-6 space-y-4 text-base">
              <li>1. Capture / Upload a cow or udder image</li>
              <li>2. YOLO11 AI analysis on the BOVIMED backend</li>
              <li>3. Risk assessment & clear recommendations</li>
              <li>4. Save history for smarter herd care</li>
            </ol>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-12 sm:px-6">
        <h2 className="font-display text-2xl font-bold">Features</h2>
        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[
            'AI-Powered Detection',
            'Camera Scan',
            'Image Upload',
            'Risk Assessment',
            'Health History',
            'Smart Recommendations',
          ].map((f) => (
            <div
              key={f}
              className="rounded-2xl border border-earth bg-white px-5 py-4 text-sm font-medium shadow-sm"
            >
              {f}
            </div>
          ))}
        </div>
        <p className="mt-10 max-w-3xl text-xs leading-relaxed text-forest/50">
          {DISCLAIMER}
        </p>
      </section>
    </div>
  )
}
