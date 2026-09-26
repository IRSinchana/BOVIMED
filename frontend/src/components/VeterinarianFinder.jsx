import { useState } from 'react'
import { MapPin, Navigation, Phone, ShieldAlert, Building2, Loader2 } from 'lucide-react'
import { useI18n } from '../i18n/I18nContext'
import { ErrorMessage } from './Status'
import { searchVeterinarians } from '../services/api'

export default function VeterinarianFinder({ initialLocation = null }) {
  const { t } = useI18n()
  const [form, setForm] = useState({
    state: initialLocation?.state || '',
    district: initialLocation?.district || '',
    city: initialLocation?.city || '',
    pincode: initialLocation?.pincode || '',
    latitude: null,
    longitude: null,
  })
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [locating, setLocating] = useState(false)

  function setField(key, value) {
    setForm((p) => ({ ...p, [key]: value }))
  }

  async function runSearch(overrides = {}) {
    setLoading(true)
    setError(null)
    const merged = { ...form, ...overrides }
    const payload = {
      state: merged.state || null,
      district: merged.district || null,
      city: merged.city || null,
      pincode: merged.pincode || null,
      latitude: merged.latitude ?? null,
      longitude: merged.longitude ?? null,
    }
    try {
      const data = await searchVeterinarians(payload)
      setResult(data)
      return data
    } catch (err) {
      setError(err.message || t.common.error)
      return null
    } finally {
      setLoading(false)
    }
  }

  async function onSearch(e) {
    e?.preventDefault()
    await runSearch()
  }

  function useMyLocation() {
    if (!navigator.geolocation) {
      setError(t.vets.geoDenied)
      return
    }

    setLocating(true)
    setError(null)

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const latitude = pos.coords.latitude
        const longitude = pos.coords.longitude
        setForm((p) => ({
          ...p,
          latitude,
          longitude,
        }))
        setLocating(false)
        // Pass browser GPS coordinates directly into the existing search flow.
        await runSearch({ latitude, longitude })
      },
      (err) => {
        setLocating(false)
        setError(t.vets.geoDenied)
        void err
      },
      {
        enableHighAccuracy: true,
        maximumAge: 0,
        timeout: 15000,
      },
    )
  }

  const providers = result?.providers || []

  return (
    <div className="space-y-6">
      <form
        onSubmit={onSearch}
        className="grid gap-4 rounded-3xl border border-earth bg-white p-5 shadow-sm sm:grid-cols-2"
      >
        <div>
          <label className="block">
            <span className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#1b4332]/70">
              {t.vets.state}
            </span>
            <input
              value={form.state}
              onChange={(e) => setField('state', e.target.value)}
              placeholder="e.g. Karnataka"
              className="w-full rounded-xl border border-earth bg-cream/30 px-4 py-2.5 text-sm text-[#1b4332] outline-none focus:border-[#2d6a4f] focus:bg-white"
            />
          </label>
        </div>

        <div>
          <label className="block">
            <span className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#1b4332]/70">
              {t.vets.district}
            </span>
            <input
              value={form.district}
              onChange={(e) => setField('district', e.target.value)}
              placeholder="e.g. Hassan"
              className="w-full rounded-xl border border-earth bg-cream/30 px-4 py-2.5 text-sm text-[#1b4332] outline-none focus:border-[#2d6a4f] focus:bg-white"
            />
          </label>
        </div>

        <div>
          <label className="block">
            <span className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#1b4332]/70">
              {t.vets.city}
            </span>
            <input
              value={form.city}
              onChange={(e) => setField('city', e.target.value)}
              placeholder="e.g. Channarayapatna"
              className="w-full rounded-xl border border-earth bg-cream/30 px-4 py-2.5 text-sm text-[#1b4332] outline-none focus:border-[#2d6a4f] focus:bg-white"
            />
          </label>
        </div>

        <div>
          <label className="block">
            <span className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#1b4332]/70">
              {t.vets.pincode}
            </span>
            <input
              value={form.pincode}
              onChange={(e) => setField('pincode', e.target.value)}
              placeholder="e.g. 573116"
              className="w-full rounded-xl border border-earth bg-cream/30 px-4 py-2.5 text-sm text-[#1b4332] outline-none focus:border-[#2d6a4f] focus:bg-white"
            />
          </label>
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3 border-t border-earth/60 pt-2 sm:col-span-2">
          <button
            type="button"
            onClick={useMyLocation}
            disabled={locating || loading}
            className="inline-flex items-center gap-2 rounded-xl border border-earth bg-cream/60 px-4 py-2.5 text-xs font-semibold text-[#1b4332] hover:bg-cream disabled:opacity-60"
          >
            {locating ? (
              <Loader2 className="h-4 w-4 animate-spin text-[#2d6a4f]" />
            ) : (
              <MapPin className="h-4 w-4 text-[#2d6a4f]" />
            )}
            {locating ? t.common.loading : t.vets.useLocation}
          </button>

          <button
            type="submit"
            disabled={loading || locating}
            className="inline-flex items-center gap-2 rounded-xl bg-[#1b4332] px-6 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-[#2d6a4f] disabled:opacity-60"
          >
            {loading ? t.vets.searching : t.vets.search}
          </button>
        </div>
      </form>

      <ErrorMessage message={error} />

      {result ? (
        <div className="space-y-4">
          <div className="rounded-2xl border border-amber-200 bg-amber-50/80 p-4 text-sm text-[#1b4332]">
            <div className="flex items-start gap-2.5">
              <ShieldAlert className="mt-0.5 h-5 w-5 shrink-0 text-amber-700" />
              <div>
                <p className="font-semibold text-amber-950">{result.message || t.vets.empty}</p>
                <p className="mt-1 text-xs font-medium text-amber-900">{t.vets.verify}</p>
                <p className="mt-1 text-[11px] text-[#1b4332]/65">{t.vets.providerNote}</p>
              </div>
            </div>
          </div>

          {providers.length === 0 ? (
            <div className="rounded-2xl border border-earth/80 bg-white p-6 text-center shadow-sm">
              <Building2 className="mx-auto h-8 w-8 text-[#1b4332]/40" />
              <p className="mt-2 text-sm text-[#1b4332]/70">{t.vets.noResults}</p>
              {result.directions_url && (
                <div className="mt-4">
                  <a
                    href={result.directions_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 rounded-xl bg-[#2d6a4f] px-5 py-2.5 text-xs font-semibold text-white shadow-sm hover:bg-[#1b4332]"
                  >
                    <Navigation className="h-4 w-4" />
                    {t.vets.directions} (Google Maps)
                  </a>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-3">
              {providers.map((p) => (
                <div
                  key={p.id || p.name}
                  className="flex flex-col justify-between gap-4 rounded-2xl border border-earth bg-white p-5 shadow-sm sm:flex-row sm:items-center"
                >
                  <div>
                    <h3 className="font-display text-base font-bold text-[#1b4332]">{p.name}</h3>
                    <p className="mt-1 text-xs text-[#1b4332]/75">{p.address}</p>
                    {p.source ? (
                      <span className="mt-1.5 inline-block rounded-full bg-cream px-2 py-0.5 text-[10px] font-medium text-[#2d6a4f]">
                        {p.source}
                      </span>
                    ) : null}
                  </div>
                  <div className="flex shrink-0 flex-wrap items-center gap-2">
                    {p.phone ? (
                      <a
                        href={`tel:${p.phone}`}
                        className="inline-flex items-center gap-1.5 rounded-xl bg-[#1b4332] px-4 py-2 text-xs font-semibold text-white"
                      >
                        <Phone className="h-3.5 w-3.5" />
                        {t.vets.call}
                      </a>
                    ) : null}
                    {result.directions_url ? (
                      <a
                        href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                          `${p.name} ${p.address || ''}`,
                        )}`}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1.5 rounded-xl border border-earth px-4 py-2 text-xs font-semibold text-[#1b4332] hover:bg-cream"
                      >
                        <Navigation className="h-3.5 w-3.5" />
                        {t.vets.directions}
                      </a>
                    ) : null}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : null}
    </div>
  )
}
