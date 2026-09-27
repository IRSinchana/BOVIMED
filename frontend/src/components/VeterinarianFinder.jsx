import { useState } from 'react'
import { MapPin, Navigation, Phone, ShieldAlert, Building2, Loader2, CheckCircle2 } from 'lucide-react'
import { useI18n } from '../i18n/I18nContext'
import { ErrorMessage } from './Status'
import { searchVeterinarians } from '../services/api'

function messageForStatus(t, data) {
  const key = data?.message_key
  if (key && t.vets?.[key]) return t.vets[key]
  if (data?.status === 'verified_found') return t.vets.foundVerified
  if (data?.status === 'location_detected_no_verified') return t.vets.noVerifiedAtLocation
  if (data?.location_detected) return t.vets.noVerifiedAtLocation
  return t.vets.noVerified
}

export default function VeterinarianFinder({ initialLocation = null }) {
  const { t, textDir } = useI18n()
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
  const [locateStatus, setLocateStatus] = useState(null)
  const [locationDetected, setLocationDetected] = useState(false)

  function setField(key, value) {
    setForm((p) => ({ ...p, [key]: value }))
  }

  async function runSearch(overrides = {}) {
    setLoading(true)
    setError(null)
    const merged = { ...form, ...overrides }
    const latitude =
      merged.latitude === null || merged.latitude === undefined || merged.latitude === ''
        ? null
        : Number(merged.latitude)
    const longitude =
      merged.longitude === null || merged.longitude === undefined || merged.longitude === ''
        ? null
        : Number(merged.longitude)

    const payload = {
      state: merged.state || null,
      district: merged.district || null,
      city: merged.city || null,
      pincode: merged.pincode || null,
      latitude: Number.isFinite(latitude) ? latitude : null,
      longitude: Number.isFinite(longitude) ? longitude : null,
    }
    try {
      const data = await searchVeterinarians(payload)
      setResult(data)
      setLocationDetected(Boolean(data?.location_detected))
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
    setLocationDetected(false)
    await runSearch()
  }

  function geoErrorMessage(err) {
    if (!err) return t.vets.geoDenied
    if (err.code === 1) return t.vets.geoDenied
    if (err.code === 2) return t.vets.geoUnavailable
    if (err.code === 3) return t.vets.geoTimeout
    return t.vets.geoDenied
  }

  function useMyLocation() {
    if (locating || loading) return
    if (!navigator.geolocation) {
      setError(t.vets.geoUnavailable)
      setLocateStatus(null)
      return
    }

    setLocating(true)
    setLocateStatus(t.vets.locating)
    setError(null)
    setResult(null)
    setLocationDetected(false)

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const latitude = pos.coords.latitude
        const longitude = pos.coords.longitude

        setForm((p) => ({
          ...p,
          latitude,
          longitude,
        }))
        setLocationDetected(true)
        setLocateStatus(t.vets.locationDetected)

        try {
          await runSearch({ latitude, longitude })
        } finally {
          setLocating(false)
          setLocateStatus(null)
        }
      },
      (err) => {
        setLocating(false)
        setLocateStatus(null)
        setLocationDetected(false)
        setError(geoErrorMessage(err))
      },
      {
        enableHighAccuracy: true,
        maximumAge: 0,
        timeout: 15000,
      },
    )
  }

  const providers = result?.providers || []
  const busy = locating || loading
  const verifiedFound = Boolean(result?.verified_found) || providers.length > 0
  const mapsUrl = result?.directions_url

  return (
    <div className="space-y-6" dir={textDir}>
      <p className="text-sm text-[#1b4332]/70">{t.vets.searchByLocation}</p>

      <form
        onSubmit={onSearch}
        className="grid gap-4 rounded-3xl border border-earth bg-white p-5 shadow-sm sm:grid-cols-2"
        dir="ltr"
      >
        <div>
          <label className="block">
            <span
              className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#1b4332]/70"
              dir={textDir}
            >
              {t.vets.state}
            </span>
            <input
              value={form.state}
              onChange={(e) => setField('state', e.target.value)}
              placeholder={t.vets.placeholderState}
              className="w-full rounded-xl border border-earth bg-cream/30 px-4 py-2.5 text-sm text-[#1b4332] outline-none focus:border-[#2d6a4f] focus:bg-white"
            />
          </label>
        </div>

        <div>
          <label className="block">
            <span
              className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#1b4332]/70"
              dir={textDir}
            >
              {t.vets.district}
            </span>
            <input
              value={form.district}
              onChange={(e) => setField('district', e.target.value)}
              placeholder={t.vets.placeholderDistrict}
              className="w-full rounded-xl border border-earth bg-cream/30 px-4 py-2.5 text-sm text-[#1b4332] outline-none focus:border-[#2d6a4f] focus:bg-white"
            />
          </label>
        </div>

        <div>
          <label className="block">
            <span
              className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#1b4332]/70"
              dir={textDir}
            >
              {t.vets.city}
            </span>
            <input
              value={form.city}
              onChange={(e) => setField('city', e.target.value)}
              placeholder={t.vets.placeholderCity}
              className="w-full rounded-xl border border-earth bg-cream/30 px-4 py-2.5 text-sm text-[#1b4332] outline-none focus:border-[#2d6a4f] focus:bg-white"
            />
          </label>
        </div>

        <div>
          <label className="block">
            <span
              className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-[#1b4332]/70"
              dir={textDir}
            >
              {t.vets.pincode}
            </span>
            <input
              value={form.pincode}
              onChange={(e) => setField('pincode', e.target.value)}
              placeholder={t.vets.placeholderPincode}
              className="w-full rounded-xl border border-earth bg-cream/30 px-4 py-2.5 text-sm text-[#1b4332] outline-none focus:border-[#2d6a4f] focus:bg-white"
            />
          </label>
        </div>

        <div className="flex flex-wrap items-center justify-between gap-3 border-t border-earth/60 pt-2 sm:col-span-2">
          <button
            type="button"
            onClick={useMyLocation}
            disabled={busy}
            className="inline-flex items-center gap-2 rounded-xl border border-earth bg-cream/60 px-4 py-2.5 text-xs font-semibold text-[#1b4332] hover:bg-cream disabled:opacity-60"
          >
            {locating ? (
              <Loader2 className="h-4 w-4 animate-spin text-[#2d6a4f]" />
            ) : (
              <MapPin className="h-4 w-4 text-[#2d6a4f]" />
            )}
            <span dir={textDir}>{locating ? t.vets.locating : t.vets.useLocation}</span>
          </button>

          <button
            type="submit"
            disabled={busy}
            className="inline-flex items-center gap-2 rounded-xl bg-[#1b4332] px-6 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-[#2d6a4f] disabled:opacity-60"
          >
            <span dir={textDir}>{loading && !locating ? t.vets.searching : t.vets.search}</span>
          </button>
        </div>

        {locateStatus ? (
          <p
            className="sm:col-span-2 flex items-center gap-2 text-xs font-medium text-[#2d6a4f]"
            dir={textDir}
          >
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
            {locateStatus}
          </p>
        ) : null}
      </form>

      <ErrorMessage message={error} />

      {result ? (
        <div className="space-y-4" dir={textDir}>
          {locationDetected || result.location_detected ? (
            <div className="flex items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50 px-3 py-2 text-xs font-semibold text-emerald-900">
              <CheckCircle2 className="h-4 w-4 shrink-0" />
              {t.vets.locationDetected}
            </div>
          ) : null}

          <div className="rounded-2xl border border-amber-200 bg-amber-50/80 p-4 text-sm text-[#1b4332]">
            <div className="flex items-start gap-2.5">
              <ShieldAlert className="mt-0.5 h-5 w-5 shrink-0 text-amber-700" />
              <div>
                <p className="font-semibold text-amber-950">{messageForStatus(t, result)}</p>
                <p className="mt-1 text-xs font-medium text-amber-900">{t.vets.verify}</p>
                <p className="mt-1 text-[11px] text-[#1b4332]/65">{t.vets.providerNote}</p>
              </div>
            </div>
          </div>

          {!verifiedFound ? (
            <div className="rounded-2xl border border-earth/80 bg-white p-6 text-center shadow-sm">
              <Building2 className="mx-auto h-8 w-8 text-[#1b4332]/40" />
              <p className="mt-2 text-sm text-[#1b4332]/70">{t.vets.noVerified}</p>
              {mapsUrl ? (
                <div className="mt-4">
                  <a
                    href={mapsUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 rounded-xl bg-[#2d6a4f] px-5 py-2.5 text-xs font-semibold text-white shadow-sm hover:bg-[#1b4332]"
                  >
                    <Navigation className="h-4 w-4" />
                    {t.vets.openMaps}
                  </a>
                </div>
              ) : null}
            </div>
          ) : (
            <div className="space-y-3">
              {providers.map((p) => (
                <div
                  key={p.id || p.name}
                  className="flex flex-col justify-between gap-4 rounded-2xl border border-earth bg-white p-5 shadow-sm sm:flex-row sm:items-center"
                  dir="ltr"
                >
                  <div dir={textDir}>
                    <h3 className="font-display text-base font-bold text-[#1b4332]">{p.name}</h3>
                    {p.address ? (
                      <p className="mt-1 text-xs text-[#1b4332]/75">{p.address}</p>
                    ) : null}
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
                        <span dir={textDir}>{t.vets.call}</span>
                      </a>
                    ) : null}
                    <a
                      href={
                        mapsUrl ||
                        `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(
                          [p.name, p.address].filter(Boolean).join(' '),
                        )}`
                      }
                      target="_blank"
                      rel="noreferrer"
                      className="inline-flex items-center gap-1.5 rounded-xl border border-earth px-4 py-2 text-xs font-semibold text-[#1b4332] hover:bg-cream"
                    >
                      <Navigation className="h-3.5 w-3.5" />
                      <span dir={textDir}>{t.vets.directions}</span>
                    </a>
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
