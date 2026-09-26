import { useI18n } from '../i18n/I18nContext'
import VeterinarianFinder from '../components/VeterinarianFinder'

export default function VeterinariansPage() {
  const { t } = useI18n()

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 className="font-display text-3xl font-bold text-[#1b4332]">{t.vets.title}</h1>
        <p className="mt-1 text-sm text-[#1b4332]/70">{t.vets.subtitle}</p>
      </div>

      <VeterinarianFinder />
    </div>
  )
}
