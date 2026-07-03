<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import WeatherHeader from './components/WeatherHeader.vue'
import SearchPanel from './components/SearchPanel.vue'
import MapPanel from './components/MapPanel.vue'
import WeatherSection from './components/WeatherSection.vue'
import SettingsPanel from './components/SettingsPanel.vue'
import AuthPanel from './components/AuthPanel.vue'
import DashboardPanel from './components/DashboardPanel.vue'
import { apiDownload, apiRequest } from './api'

const DEFAULT_LOCATION_QUERY = 'San Francisco'
const STORAGE_KEYS = {
  language: 'weather-app.language',
  temperatureUnit: 'weather-app.temperature-unit',
}

const WEATHER_ICONS = {
  clear: '☀️',
  'partly-cloudy': '⛅',
  cloudy: '☁️',
  fog: '🌫️',
  drizzle: '🌦️',
  rain: '🌧️',
  showers: '🌦️',
  snow: '❄️',
  storm: '⛈️',
  unknown: '🌤️',
}

const TRANSLATIONS = {
  English: {
    statuses: {
      default: 'Showing a default location while you choose your own.',
      searchPrompt: 'Enter a location to see details',
      settingsSaved: (language, unit) => `Settings updated: ${language}, ${unit}`,
      weatherLoaded: (location) => `Showing weather for ${location}`,
      currentLocationLoaded: 'Showing weather for your current location',
      signedIn: (email) => `Signed in as ${email}`,
      registered: (email) => `Registered as ${email}`,
      signedOut: 'Signed out',
      dashboardSignIn: 'Sign in to open the dashboard',
      recordDeleted: 'Record deleted',
      recordUpdated: (status) => `Record marked as ${status}`,
      exportDone: (format) => `Exported records as ${format.toUpperCase()}`,
      customRangeLoaded: (location) => `Custom range loaded for ${location}`,
    },
    tips: {
      currentLocationSignIn: 'Sign in to save searches and unlock custom date-range history.',
      customRangeSignIn: 'Sign in to unlock custom date-range lookups, saved history, and exports.',
      futureRange: 'Choose dates on or before today for past observed weather. Use Now or 5 Day for current and future conditions.',
      blankAuth: 'Email and password are both required.',
    },
    header: {
      eyebrow: 'Weather demo',
      dashboard: 'Dashboard',
      settings: 'Settings',
      signIn: 'Sign In',
      signOutFallback: 'Sign Out',
      home: 'Home',
    },
    search: {
      eyebrow: 'Search',
      title: 'Find weather by location',
      description: 'Enter a city, zip code, landmark, or coordinates. Suggestions will appear while you type.',
      placeholder: 'Try: Tokyo, 10001, Golden Gate Bridge',
      submit: 'Submit',
      loading: 'Loading...',
      currentLocation: 'Use my current location',
      currentLocationLoading: 'Locating...',
      suggestions: 'Suggestions',
      city: 'City / town',
      zip: 'Zip code',
      coordinates: 'Coordinates',
    },
    map: {
      eyebrow: 'Map preview',
      title: 'Location area',
      fallback: 'Resolved location details will appear here.',
      openStreetMap: 'Open larger map',
    },
    weather: {
      eyebrow: 'Weather',
      title: 'Current conditions',
      now: 'Now',
      forecast: '5 Day',
      customRange: 'Custom range',
      location: 'Location',
      currentWeather: 'Current weather',
      usefulDetails: 'Useful details',
      customEyebrow: 'Custom range',
      customTitle: 'Choose a date range',
      startDate: 'Start date',
      endDate: 'End date',
      checkRange: 'Check range',
      average: 'Average',
      highLow: 'High',
      day: 'Day',
      night: 'Night',
    },
    auth: {
      eyebrow: 'Account',
      signInTitle: 'Sign in',
      registerTitle: 'Register',
      email: 'Email',
      password: 'Password',
      signIn: 'Sign In',
      register: 'Register',
      close: 'Close',
      wait: 'Please wait...',
      noAccount: "Don't have an account?",
      haveAccount: 'Already have an account?',
    },
    settings: {
      eyebrow: 'Settings',
      title: 'Display options',
      language: 'Language',
      temperature: 'Temperature',
      save: 'Save settings',
      close: 'Close',
      celsius: 'Celsius',
      fahrenheit: 'Fahrenheit',
    },
    dashboard: {
      eyebrow: 'User workspace',
      title: 'Saved weather records',
      back: 'Back to home',
      records: 'Records',
      unit: 'Unit',
      export: 'Export',
      exportLabel: 'Export data',
      exportTitle: 'Download saved weather records',
      helper: 'No saved records yet. Sign in and search or save a custom date range to populate the dashboard.',
      loading: 'Loading saved records...',
      location: 'Location',
      dateRange: 'Date range',
      temp: 'Temp',
      status: 'Status',
      actions: 'Actions',
      edit: 'Edit',
      delete: 'Delete',
      currentWeather: 'Current weather',
    },
  },
  Spanish: {
    statuses: {
      default: 'Mostrando una ubicacion predeterminada mientras eliges la tuya.',
      searchPrompt: 'Ingresa una ubicacion para ver detalles',
      settingsSaved: (language, unit) => `Configuracion actualizada: ${language}, ${unit}`,
      weatherLoaded: (location) => `Mostrando el clima de ${location}`,
      currentLocationLoaded: 'Mostrando el clima de tu ubicacion actual',
      signedIn: (email) => `Sesion iniciada como ${email}`,
      registered: (email) => `Registro completado como ${email}`,
      signedOut: 'Sesion cerrada',
      dashboardSignIn: 'Inicia sesion para abrir el panel',
      recordDeleted: 'Registro eliminado',
      recordUpdated: (status) => `Registro marcado como ${status}`,
      exportDone: (format) => `Registros exportados como ${format.toUpperCase()}`,
      customRangeLoaded: (location) => `Rango personalizado cargado para ${location}`,
    },
    tips: {
      currentLocationSignIn: 'Inicia sesion para guardar busquedas y desbloquear el historial por rango de fechas.',
      customRangeSignIn: 'Inicia sesion para desbloquear busquedas por rango, historial guardado y exportaciones.',
      futureRange: 'Elige fechas de hoy o anteriores para el clima observado. Usa Ahora o 5 dias para condiciones actuales y futuras.',
      blankAuth: 'Correo y contrasena son obligatorios.',
    },
    header: { eyebrow: 'Demo del clima', dashboard: 'Panel', settings: 'Ajustes', signIn: 'Entrar', signOutFallback: 'Salir', home: 'Inicio' },
    search: { eyebrow: 'Busqueda', title: 'Busca el clima por ubicacion', description: 'Ingresa ciudad, codigo postal, punto de interes o coordenadas. Las sugerencias aparecen mientras escribes.', placeholder: 'Prueba: Tokyo, 10001, Golden Gate Bridge', submit: 'Buscar', loading: 'Cargando...', currentLocation: 'Usar mi ubicacion actual', currentLocationLoading: 'Ubicando...', suggestions: 'Sugerencias', city: 'Ciudad / pueblo', zip: 'Codigo postal', coordinates: 'Coordenadas' },
    map: { eyebrow: 'Mapa', title: 'Area de ubicacion', fallback: 'Los detalles resueltos apareceran aqui.', openStreetMap: 'Abrir mapa grande' },
    weather: { eyebrow: 'Clima', title: 'Condiciones actuales', now: 'Ahora', forecast: '5 dias', customRange: 'Rango', location: 'Ubicacion', currentWeather: 'Clima actual', usefulDetails: 'Detalles utiles', customEyebrow: 'Rango personalizado', customTitle: 'Elige un rango de fechas', startDate: 'Fecha inicial', endDate: 'Fecha final', checkRange: 'Consultar rango', average: 'Promedio', highLow: 'Alta', day: 'Dia', night: 'Noche' },
    auth: { eyebrow: 'Cuenta', signInTitle: 'Entrar', registerTitle: 'Registrarse', email: 'Correo', password: 'Contrasena', signIn: 'Entrar', register: 'Registrarse', close: 'Cerrar', wait: 'Espera...', noAccount: 'No tienes cuenta?', haveAccount: 'Ya tienes cuenta?' },
    settings: { eyebrow: 'Ajustes', title: 'Opciones de pantalla', language: 'Idioma', temperature: 'Temperatura', save: 'Guardar ajustes', close: 'Cerrar', celsius: 'Celsius', fahrenheit: 'Fahrenheit' },
    dashboard: { eyebrow: 'Espacio del usuario', title: 'Registros guardados', back: 'Volver al inicio', records: 'Registros', unit: 'Unidad', export: 'Exportar', exportLabel: 'Exportar datos', exportTitle: 'Descargar registros guardados', helper: 'Aun no hay registros guardados. Inicia sesion y busca o guarda un rango para llenar el panel.', loading: 'Cargando registros...', location: 'Ubicacion', dateRange: 'Rango de fechas', temp: 'Temp', status: 'Estado', actions: 'Acciones', edit: 'Editar', delete: 'Eliminar', currentWeather: 'Clima actual' },
  },
  French: {
    statuses: { default: 'Affichage dun lieu par defaut pendant que vous choisissez le votre.', searchPrompt: 'Saisissez un lieu pour voir les details', settingsSaved: (language, unit) => `Parametres mis a jour : ${language}, ${unit}`, weatherLoaded: (location) => `Affichage de la meteo pour ${location}`, currentLocationLoaded: 'Affichage de la meteo pour votre position actuelle', signedIn: (email) => `Connecte comme ${email}`, registered: (email) => `Compte cree pour ${email}`, signedOut: 'Deconnecte', dashboardSignIn: 'Connectez-vous pour ouvrir le tableau de bord', recordDeleted: 'Enregistrement supprime', recordUpdated: (status) => `Enregistrement marque comme ${status}`, exportDone: (format) => `Enregistrements exportes en ${format.toUpperCase()}`, customRangeLoaded: (location) => `Plage personnalisee chargee pour ${location}` },
    tips: { currentLocationSignIn: 'Connectez-vous pour enregistrer les recherches et utiliser lhistorique par plage de dates.', customRangeSignIn: 'Connectez-vous pour debloquer les recherches par plage, lhistorique et les exports.', futureRange: 'Choisissez des dates aujourdhui ou avant pour la meteo observee. Utilisez Maintenant ou 5 jours pour les conditions actuelles et futures.', blankAuth: 'E-mail et mot de passe sont obligatoires.' },
    header: { eyebrow: 'Demo meteo', dashboard: 'Tableau', settings: 'Parametres', signIn: 'Connexion', signOutFallback: 'Deconnexion', home: 'Accueil' },
    search: { eyebrow: 'Recherche', title: 'Trouver la meteo par lieu', description: 'Saisissez une ville, un code postal, un point dinteret ou des coordonnees. Les suggestions apparaissent pendant la saisie.', placeholder: 'Exemple : Tokyo, 10001, Golden Gate Bridge', submit: 'Rechercher', loading: 'Chargement...', currentLocation: 'Utiliser ma position', currentLocationLoading: 'Localisation...', suggestions: 'Suggestions', city: 'Ville / village', zip: 'Code postal', coordinates: 'Coordonnees' },
    map: { eyebrow: 'Carte', title: 'Zone de localisation', fallback: 'Les details resolus apparaitront ici.', openStreetMap: 'Ouvrir la grande carte' },
    weather: { eyebrow: 'Meteo', title: 'Conditions actuelles', now: 'Maintenant', forecast: '5 jours', customRange: 'Plage', location: 'Lieu', currentWeather: 'Meteo actuelle', usefulDetails: 'Details utiles', customEyebrow: 'Plage personnalisee', customTitle: 'Choisissez une plage de dates', startDate: 'Date de debut', endDate: 'Date de fin', checkRange: 'Verifier la plage', average: 'Moyenne', highLow: 'Max', day: 'Jour', night: 'Nuit' },
    auth: { eyebrow: 'Compte', signInTitle: 'Connexion', registerTitle: 'Inscription', email: 'E-mail', password: 'Mot de passe', signIn: 'Connexion', register: 'Inscription', close: 'Fermer', wait: 'Veuillez patienter...', noAccount: 'Pas de compte ?', haveAccount: 'Vous avez deja un compte ?' },
    settings: { eyebrow: 'Parametres', title: 'Options daffichage', language: 'Langue', temperature: 'Temperature', save: 'Enregistrer', close: 'Fermer', celsius: 'Celsius', fahrenheit: 'Fahrenheit' },
    dashboard: { eyebrow: 'Espace utilisateur', title: 'Enregistrements sauvegardes', back: 'Retour a laccueil', records: 'Enregistrements', unit: 'Unite', export: 'Export', exportLabel: 'Exporter les donnees', exportTitle: 'Telecharger les enregistrements', helper: 'Aucun enregistrement pour le moment. Connectez-vous puis recherchez ou enregistrez une plage de dates.', loading: 'Chargement des enregistrements...', location: 'Lieu', dateRange: 'Plage de dates', temp: 'Temp', status: 'Statut', actions: 'Actions', edit: 'Modifier', delete: 'Supprimer', currentWeather: 'Meteo actuelle' },
  },
  Chinese: {
    statuses: { default: '当前显示默认地点，你可以随时切换。', searchPrompt: '请输入地点查看天气详情', settingsSaved: (language, unit) => `设置已更新：${language}，${unit}`, weatherLoaded: (location) => `正在显示 ${location} 的天气`, currentLocationLoaded: '正在显示你当前位置的天气', signedIn: (email) => `已登录：${email}`, registered: (email) => `已注册：${email}`, signedOut: '已退出登录', dashboardSignIn: '请先登录后再打开控制台', recordDeleted: '记录已删除', recordUpdated: (status) => `记录状态已更新为 ${status}`, exportDone: (format) => `已导出 ${format.toUpperCase()} 格式记录`, customRangeLoaded: (location) => `已加载 ${location} 的自定义日期范围天气` },
    tips: { currentLocationSignIn: '登录后可保存搜索记录，并解锁自定义日期范围历史功能。', customRangeSignIn: '请先登录以解锁自定义日期范围、历史记录和导出功能。', futureRange: '历史天气只能查询今天及以前的日期。当前或未来天气请使用“Now”或“5 Day”。', blankAuth: '邮箱和密码都不能为空。' },
    header: { eyebrow: '天气演示', dashboard: '控制台', settings: '设置', signIn: '登录', signOutFallback: '退出', home: '首页' },
    search: { eyebrow: '搜索', title: '按地点查询天气', description: '输入城市、邮编、地标或坐标，输入时会自动显示模糊建议。', placeholder: '例如：Tokyo, 10001, Golden Gate Bridge', submit: '查询', loading: '加载中...', currentLocation: '使用当前位置', currentLocationLoading: '定位中...', suggestions: '建议', city: '城市 / 城镇', zip: '邮编', coordinates: '坐标' },
    map: { eyebrow: '地图', title: '位置区域', fallback: '解析后的地点信息会显示在这里。', openStreetMap: '打开大地图' },
    weather: { eyebrow: '天气', title: '当前天气', now: '当前', forecast: '5天', customRange: '自定义', location: '位置', currentWeather: '当前天气', usefulDetails: '更多信息', customEyebrow: '自定义日期', customTitle: '选择日期范围', startDate: '开始日期', endDate: '结束日期', checkRange: '查询范围', average: '平均', highLow: '最高', day: '白天', night: '夜间' },
    auth: { eyebrow: '账号', signInTitle: '登录', registerTitle: '注册', email: '邮箱', password: '密码', signIn: '登录', register: '注册', close: '关闭', wait: '请稍候...', noAccount: '还没有账号？', haveAccount: '已经有账号？' },
    settings: { eyebrow: '设置', title: '显示选项', language: '语言', temperature: '温度', save: '保存设置', close: '关闭', celsius: '摄氏', fahrenheit: '华氏' },
    dashboard: { eyebrow: '用户空间', title: '已保存天气记录', back: '返回首页', records: '记录数', unit: '单位', export: '导出', exportLabel: '导出数据', exportTitle: '下载保存的天气记录', helper: '当前还没有保存记录。请先登录后搜索或保存日期范围。', loading: '正在加载记录...', location: '地点', dateRange: '日期范围', temp: '温度', status: '状态', actions: '操作', edit: '编辑', delete: '删除', currentWeather: '当前天气' },
  },
}

const activeView = ref('now')
const selectedLocation = ref(DEFAULT_LOCATION_QUERY)
const activeLocationQuery = ref(DEFAULT_LOCATION_QUERY)
const statusText = ref('')
const searchQuery = ref(DEFAULT_LOCATION_QUERY)
const searchError = ref('')
const showSettings = ref(false)
const showAuthPanel = ref(false)
const authMode = ref('signin')
const temperatureUnit = ref('C')
const language = ref('English')
const activePage = ref('home')
const isAuthenticated = ref(false)
const authUser = ref(null)
const isSearching = ref(false)
const isCurrentLocationLoading = ref(false)
const isDashboardLoading = ref(false)
const isAuthLoading = ref(false)
const weatherError = ref('')
const dashboardError = ref('')
const authError = ref('')
const locationSuggestions = ref([])
let suggestionTimer = null

const currentWeather = reactive({
  location: DEFAULT_LOCATION_QUERY,
  region: 'California, United States',
  temperatureC: null,
  condition: 'Waiting for lookup',
  feelsLikeC: null,
  humidity: 'Humidity unavailable',
  wind: 'Wind unavailable',
  icon: '🌤️',
  latitude: 37.7749,
  longitude: -122.4194,
  source: '',
})

const forecastDays = ref([])
const savedWeatherRecords = ref([])
const rangeDays = ref([])
const rangeSummary = ref(null)
const customRange = reactive({ startDate: '', endDate: '' })

const messages = computed(() => TRANSLATIONS[language.value] ?? TRANSLATIONS.English)
const formattedCurrentTemp = computed(() => formatTemperature(currentWeather.temperatureC, temperatureUnit.value))
const formattedFeelsLike = computed(() => currentWeather.feelsLikeC == null ? fallbackText('Feels like unavailable') : `${fallbackText('Feels like')} ${formatTemperature(currentWeather.feelsLikeC, temperatureUnit.value)}`)
const formattedForecastDays = computed(() => buildForecastPresentation(forecastDays.value))
const formattedRangeDays = computed(() => buildForecastPresentation(rangeDays.value))
const formattedRangeSummary = computed(() => {
  if (!rangeSummary.value) {
    return null
  }
  return {
    ...rangeSummary.value,
    averageTemp: formatTemperature(rangeSummary.value.average_temp_c, temperatureUnit.value),
    maxTemp: formatTemperature(rangeSummary.value.max_temp_c, temperatureUnit.value),
    minTemp: formatTemperature(rangeSummary.value.min_temp_c, temperatureUnit.value),
  }
})

function fallbackText(value) {
  return value
}

function buildForecastPresentation(items) {
  return items.map((item) => ({
    ...item,
    day: formatWeekday(item.date),
    dateLabel: formatDateLabel(item.date),
    temp: formatRangeTemperature(item.temp_min_c, item.temp_max_c, temperatureUnit.value),
    dayInfo: `${item.condition}${item.temp_max_c != null ? ` with highs near ${formatTemperature(item.temp_max_c, temperatureUnit.value)}` : ''}`,
    nightInfo: item.temp_min_c != null ? `Lows around ${formatTemperature(item.temp_min_c, temperatureUnit.value)}.` : 'Night details unavailable.',
  }))
}

function formatTemperature(value, unit) {
  if (value == null || Number.isNaN(value)) {
    return '--'
  }
  if (unit === 'F') {
    return `${Math.round((value * 9) / 5 + 32)}°F`
  }
  return `${Math.round(value)}°C`
}

function formatRangeTemperature(minValue, maxValue, unit) {
  const low = formatTemperature(minValue, unit)
  const high = formatTemperature(maxValue, unit)
  if (low === '--' && high === '--') {
    return '--'
  }
  return `${low} to ${high}`
}

function formatWeekday(value) {
  return new Date(`${value}T00:00:00`).toLocaleDateString(languageTag(language.value), { weekday: 'short' })
}

function formatDateLabel(value) {
  return new Date(`${value}T00:00:00`).toLocaleDateString(languageTag(language.value), { month: 'short', day: 'numeric' })
}

function languageTag(languageName) {
  return {
    English: 'en-US',
    Spanish: 'es-ES',
    French: 'fr-FR',
    Chinese: 'zh-CN',
  }[languageName] ?? 'en-US'
}

function weatherIcon(code) {
  return WEATHER_ICONS[code] ?? WEATHER_ICONS.unknown
}

function readStorage(key, fallback) {
  try {
    return window.localStorage.getItem(key) ?? fallback
  } catch {
    return fallback
  }
}

function writeStorage(key, value) {
  try {
    window.localStorage.setItem(key, value)
  } catch {
  }
}

function loadSettings() {
  language.value = readStorage(STORAGE_KEYS.language, language.value)
  temperatureUnit.value = readStorage(STORAGE_KEYS.temperatureUnit, temperatureUnit.value)
  statusText.value = messages.value.statuses.default
}

function handleGlobalKeydown(event) {
  if (event.key !== 'Escape') return
  if (showAuthPanel.value) {
    closeAuth()
    return
  }
  if (showSettings.value) closeSettings()
}

function normalizeCurrentWeather(payload) {
  selectedLocation.value = payload.location.display_label
  currentWeather.location = payload.location.name
  currentWeather.region = [payload.location.region, payload.location.country].filter(Boolean).join(', ') || payload.location.display_label
  currentWeather.temperatureC = payload.current?.temperature_c ?? null
  currentWeather.condition = payload.current?.condition ?? 'Weather unavailable'
  currentWeather.feelsLikeC = payload.current?.feels_like_c ?? null
  currentWeather.humidity = payload.current?.humidity != null ? `Humidity ${Math.round(payload.current.humidity)}%` : 'Humidity unavailable'
  currentWeather.wind = payload.current?.wind_speed != null ? `Wind ${Math.round(payload.current.wind_speed)} km/h` : 'Wind unavailable'
  currentWeather.icon = weatherIcon(payload.current?.icon_code)
  currentWeather.latitude = payload.location.latitude
  currentWeather.longitude = payload.location.longitude
  currentWeather.source = payload.source
}

async function fetchCurrentWeather(location) {
  const payload = await apiRequest(`/weather/current?location=${encodeURIComponent(location)}`)
  normalizeCurrentWeather(payload)
  return payload
}

async function fetchForecast(location) {
  const payload = await apiRequest(`/weather/forecast?location=${encodeURIComponent(location)}&days=5`)
  forecastDays.value = payload.forecast_days
}

async function fetchHistory() {
  const payload = await apiRequest('/weather/history')
  savedWeatherRecords.value = payload.records.map((record) => ({
    id: record.id,
    location: record.resolved_name,
    startDate: record.start_date ?? messages.value.dashboard.currentWeather,
    endDate: record.end_date ?? messages.value.dashboard.currentWeather,
    temperature: historyTemperature(record.weather_payload),
    status: record.status,
    notes: record.notes,
    weather_payload: record.weather_payload,
  }))
}

function historyTemperature(payload) {
  if (payload?.current?.temperature_c != null) {
    return formatTemperature(payload.current.temperature_c, temperatureUnit.value)
  }
  if (payload?.range_summary?.average_temp_c != null) {
    return `${messages.value.weather.average} ${formatTemperature(payload.range_summary.average_temp_c, temperatureUnit.value)}`
  }
  return '--'
}

async function saveCurrentSearchRecord(locationQuery) {
  if (!isAuthenticated.value) return
  await apiRequest('/weather/history', {
    method: 'POST',
    body: JSON.stringify({
      location: locationQuery,
      status: 'Active',
    }),
  })
}

async function handleSearch(query, options = {}) {
  const normalizedQuery = query.trim()
  searchQuery.value = normalizedQuery

  if (!normalizedQuery) {
    searchError.value = 'Please enter a location before searching.'
    statusText.value = messages.value.statuses.searchPrompt
    return
  }

  isSearching.value = true
  searchError.value = ''
  weatherError.value = ''
  rangeSummary.value = null
  rangeDays.value = []
  activeLocationQuery.value = normalizedQuery

  try {
    await fetchCurrentWeather(normalizedQuery)
    await fetchForecast(normalizedQuery)
    statusText.value = messages.value.statuses.weatherLoaded(selectedLocation.value)
    if (options.persist) {
      await saveCurrentSearchRecord(normalizedQuery)
      await fetchHistory()
    }
  } catch (error) {
    searchError.value = error.message || 'Unable to fetch weather for that location.'
    statusText.value = 'Location lookup failed'
  } finally {
    isSearching.value = false
  }
}

async function handleCurrentLocation() {
  if (!navigator.geolocation) {
    searchError.value = 'Your browser does not support current-location lookup.'
    return
  }

  isCurrentLocationLoading.value = true
  searchError.value = ''
  weatherError.value = ''
  rangeSummary.value = null
  rangeDays.value = []

  try {
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject, { enableHighAccuracy: true, timeout: 15000 })
    })
    const { latitude, longitude } = position.coords
    activeLocationQuery.value = `${latitude}, ${longitude}`
    const payload = await apiRequest(`/weather/current-location?lat=${latitude}&lon=${longitude}`)
    normalizeCurrentWeather(payload)
    await fetchForecast(activeLocationQuery.value)
    statusText.value = messages.value.statuses.currentLocationLoaded
    if (isAuthenticated.value) {
      await saveCurrentSearchRecord(activeLocationQuery.value)
      await fetchHistory()
    } else {
      weatherError.value = messages.value.tips.currentLocationSignIn
      openAuth('signin')
    }
  } catch (error) {
    searchError.value = error.message || 'Unable to determine your current location.'
    statusText.value = 'Current-location lookup failed'
  } finally {
    isCurrentLocationLoading.value = false
  }
}

function setActiveView(view) {
  activeView.value = view
}

function isFutureDate(dateValue) {
  const today = new Date()
  const localToday = new Date(today.getFullYear(), today.getMonth(), today.getDate())
  return new Date(`${dateValue}T00:00:00`) > localToday
}

async function handleRangeSubmit(payload) {
  customRange.startDate = payload.startDate
  customRange.endDate = payload.endDate

  if (!payload.startDate || !payload.endDate) {
    weatherError.value = 'Please choose both a start date and an end date.'
    return
  }
  if (payload.startDate > payload.endDate) {
    weatherError.value = 'Start date must be before or equal to end date.'
    return
  }
  if (isFutureDate(payload.startDate) || isFutureDate(payload.endDate)) {
    weatherError.value = messages.value.tips.futureRange
    return
  }
  if (!isAuthenticated.value) {
    weatherError.value = messages.value.tips.customRangeSignIn
    openAuth('signin')
    return
  }

  weatherError.value = ''

  try {
    const targetLocation = activeLocationQuery.value || searchQuery.value.trim() || DEFAULT_LOCATION_QUERY
    const result = await apiRequest(`/weather/range?location=${encodeURIComponent(targetLocation)}&start_date=${payload.startDate}&end_date=${payload.endDate}`)
    rangeSummary.value = result.range_summary
    rangeDays.value = result.forecast_days
    selectedLocation.value = result.location.display_label
    currentWeather.region = [result.location.region, result.location.country].filter(Boolean).join(', ') || result.location.display_label
    currentWeather.latitude = result.location.latitude
    currentWeather.longitude = result.location.longitude
    statusText.value = messages.value.statuses.customRangeLoaded(selectedLocation.value)

    await apiRequest('/weather/history', {
      method: 'POST',
      body: JSON.stringify({
        location: targetLocation,
        start_date: payload.startDate,
        end_date: payload.endDate,
        status: 'Saved',
      }),
    })
    await fetchHistory()
  } catch (error) {
    weatherError.value = error.message || messages.value.tips.futureRange
  }
}

function openSettings() { showSettings.value = true }
function closeSettings() { showSettings.value = false }

function saveSettings(payload) {
  temperatureUnit.value = payload.temperatureUnit
  language.value = payload.language
  writeStorage(STORAGE_KEYS.language, language.value)
  writeStorage(STORAGE_KEYS.temperatureUnit, temperatureUnit.value)
  showSettings.value = false
  statusText.value = messages.value.statuses.settingsSaved(language.value, temperatureUnit.value)
}

function openAuth(mode) {
  authError.value = ''
  authMode.value = mode
  showAuthPanel.value = true
}
function closeAuth() { showAuthPanel.value = false }
function switchAuthMode(mode) { authError.value = ''; authMode.value = mode }

async function submitAuth(payload) {
  const email = payload.email.trim()
  const password = payload.password.trim()
  if (!email || !password) {
    authError.value = messages.value.tips.blankAuth
    return
  }

  isAuthLoading.value = true
  authError.value = ''
  try {
    const path = payload.mode === 'signin' ? '/auth/login' : '/auth/register'
    const result = await apiRequest(path, {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
    authUser.value = result.user
    isAuthenticated.value = true
    showAuthPanel.value = false
    statusText.value = payload.mode === 'signin' ? messages.value.statuses.signedIn(result.user.email) : messages.value.statuses.registered(result.user.email)
    activePage.value = 'dashboard'
    await fetchHistory()
  } catch (error) {
    authError.value = error.message || 'Authentication failed.'
  } finally {
    isAuthLoading.value = false
  }
}

async function logout() {
  try {
    await apiRequest('/auth/logout', { method: 'POST' })
  } finally {
    isAuthenticated.value = false
    authUser.value = null
    savedWeatherRecords.value = []
    activePage.value = 'home'
    statusText.value = messages.value.statuses.signedOut
  }
}

async function openDashboard() {
  if (!isAuthenticated.value) {
    openAuth('signin')
    statusText.value = messages.value.statuses.dashboardSignIn
    return
  }
  activePage.value = 'dashboard'
  isDashboardLoading.value = true
  dashboardError.value = ''
  try {
    await fetchHistory()
  } catch (error) {
    dashboardError.value = error.message || 'Unable to load saved weather records.'
  } finally {
    isDashboardLoading.value = false
  }
}

function backToHome() { activePage.value = 'home' }

async function removeRecord(recordId) {
  try {
    await apiRequest(`/weather/history/${recordId}`, { method: 'DELETE' })
    savedWeatherRecords.value = savedWeatherRecords.value.filter((item) => item.id !== recordId)
    statusText.value = messages.value.statuses.recordDeleted
  } catch (error) {
    dashboardError.value = error.message || 'Unable to delete that record.'
  }
}

async function exportRecords(format) {
  try {
    const response = await apiDownload(`/weather/export?format=${format}`)
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = `weather-history.${format === 'markdown' ? 'md' : format}`
    document.body.appendChild(anchor)
    anchor.click()
    anchor.remove()
    window.URL.revokeObjectURL(url)
    statusText.value = messages.value.statuses.exportDone(format)
  } catch (error) {
    dashboardError.value = error.message || 'Unable to export records.'
  }
}

async function updateRecord(recordId) {
  const target = savedWeatherRecords.value.find((item) => item.id === recordId)
  if (!target) return
  const nextStatus = target.status === 'Active' ? 'Saved' : 'Active'
  try {
    await apiRequest(`/weather/history/${recordId}`, { method: 'PATCH', body: JSON.stringify({ status: nextStatus }) })
    target.status = nextStatus
    statusText.value = messages.value.statuses.recordUpdated(nextStatus)
  } catch (error) {
    dashboardError.value = error.message || 'Unable to update that record.'
  }
}

async function loadAuthState() {
  try {
    const payload = await apiRequest('/auth/me')
    authUser.value = payload.user
    isAuthenticated.value = true
  } catch {
    authUser.value = null
    isAuthenticated.value = false
  }
}

function chooseSuggestion(suggestion) {
  searchQuery.value = suggestion.display_label
  locationSuggestions.value = []
  handleSearch(suggestion.display_label, { persist: true })
}

async function fetchSuggestions(query) {
  const trimmed = query.trim()
  if (trimmed.length < 2) {
    locationSuggestions.value = []
    return
  }
  try {
    const payload = await apiRequest(`/locations/search?query=${encodeURIComponent(trimmed)}`)
    locationSuggestions.value = payload.results ?? []
  } catch {
    locationSuggestions.value = []
  }
}

watch(searchQuery, (value) => {
  if (suggestionTimer) {
    window.clearTimeout(suggestionTimer)
  }
  suggestionTimer = window.setTimeout(() => {
    fetchSuggestions(value)
  }, 250)
})

watch(temperatureUnit, () => {
  savedWeatherRecords.value = savedWeatherRecords.value.map((record) => ({
    ...record,
    temperature: historyTemperature(record.weather_payload),
  }))
})

watch(language, () => {
  document.documentElement.lang = languageTag(language.value)
})

onMounted(async () => {
  loadSettings()
  document.documentElement.lang = languageTag(language.value)
  window.addEventListener('keydown', handleGlobalKeydown)
  await loadAuthState()
  await handleSearch(DEFAULT_LOCATION_QUERY, { persist: false })
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleGlobalKeydown)
  if (suggestionTimer) {
    window.clearTimeout(suggestionTimer)
  }
})
</script>

<template>
  <div class="page-shell">
    <WeatherHeader
      :selected-location="selectedLocation"
      :status-text="statusText"
      :temperature-unit="temperatureUnit"
      :is-authenticated="isAuthenticated"
      :user-email="authUser?.email ?? ''"
      :labels="messages.header"
      @open-settings="openSettings"
      @open-auth="openAuth('signin')"
      @open-dashboard="openDashboard"
      @home="backToHome"
      @logout="logout"
    />

    <template v-if="activePage === 'home'">
      <main class="top-grid">
        <SearchPanel
          v-model:query="searchQuery"
          :error-message="searchError"
          :loading="isSearching"
          :current-location-loading="isCurrentLocationLoading"
          :suggestions="locationSuggestions"
          :labels="messages.search"
          @search="(value) => handleSearch(value, { persist: true })"
          @use-current-location="handleCurrentLocation"
          @select-suggestion="chooseSuggestion"
        />

        <MapPanel
          :location-label="selectedLocation"
          :region-label="currentWeather.region"
          :latitude="currentWeather.latitude"
          :longitude="currentWeather.longitude"
          :labels="messages.map"
        />
      </main>

      <WeatherSection
        :active-view="activeView"
        :selected-location="selectedLocation"
        :current-weather="currentWeather"
        :forecast-days="formattedForecastDays"
        :custom-range="customRange"
        :range-days="formattedRangeDays"
        :range-summary="formattedRangeSummary"
        :temperature-unit="temperatureUnit"
        :current-temperature="formattedCurrentTemp"
        :feels-like-text="formattedFeelsLike"
        :error-message="weatherError"
        :labels="messages.weather"
        @change-view="setActiveView"
        @submit-range="handleRangeSubmit"
      />
    </template>

    <DashboardPanel
      v-else
      :records="savedWeatherRecords"
      :temperature-unit="temperatureUnit"
      :loading="isDashboardLoading"
      :error-message="dashboardError"
      :labels="messages.dashboard"
      @back="backToHome"
      @update-record="updateRecord"
      @delete-record="removeRecord"
      @export-records="exportRecords"
    />

    <SettingsPanel
      v-if="showSettings"
      :language="language"
      :temperature-unit="temperatureUnit"
      :labels="messages.settings"
      @close="closeSettings"
      @save="saveSettings"
    />

    <AuthPanel
      v-if="showAuthPanel"
      :mode="authMode"
      :loading="isAuthLoading"
      :error-message="authError"
      :labels="messages.auth"
      @close="closeAuth"
      @switch-mode="switchAuthMode"
      @submit="submitAuth"
    />
  </div>
</template>

<style scoped>
:global(*) { box-sizing: border-box; }
:global(body) {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
  background: #f5f8f4;
  color: #17311f;
}
:global(button), :global(input), :global(select) { font: inherit; }
.page-shell {
  width: min(1180px, calc(100% - 32px));
  margin: 24px auto 40px;
  display: grid;
  gap: 20px;
  position: relative;
}
.top-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(320px, 0.75fr);
  gap: 20px;
}
@media (max-width: 960px) {
  .top-grid { grid-template-columns: 1fr; }
}
</style>
