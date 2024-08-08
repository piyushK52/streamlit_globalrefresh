import { Streamlit, RenderData } from "streamlit-component-lib"

let global_count = 0

interface RefreshActiveChangedEventDetail {
  active: boolean
  hasChanged: boolean
}

declare global {
  interface WindowEventMap {
    refreshLockChanged: CustomEvent<boolean>
    refreshActiveChanged: CustomEvent<RefreshActiveChangedEventDetail>
  }
}

class Args {
  limit: number | null = null
  interval: number | null = null
  key: string | null = null
  lock_expiration: number | null = 30000 // this is here basically to prevent an old lock from blocking all the code

  setLimit(limit: number | null) {
    const hasChanged = this.limit !== limit
    this.limit = limit
    return hasChanged
  }

  setLockExpiration(le: number | null) {
    const hasChanged = this.lock_expiration !== le
    this.lock_expiration = le
    return hasChanged
  }

  setInterval(intervalTime: number) {
    const hasChanged = this.interval !== intervalTime
    this.interval = intervalTime
    return hasChanged
  }

  setKey(key: string | null) {
    const hasChanged = this.key !== key
    this.key = key
    return hasChanged
  }
}

const widget_args = new Args()
let interval: number | null = null

const LOCK_KEY = "shared_refresh_lock"
const LOCK_TIMESTAMP_KEY = "shared_refresh_lock_timestamp"
// const REFRESH_ACTIVE_KEY = 'shared_refresh_active'

function isLocked(): boolean {
  const lockTimestamp = parseInt(
    localStorage.getItem(LOCK_TIMESTAMP_KEY) || "0",
    0
  )
  const currentTime = Date.now()

  // console.log("time diff: ", currentTime - lockTimestamp, currentTime, lockTimestamp)
  if (
    widget_args.lock_expiration !== null &&
    currentTime - lockTimestamp > widget_args.lock_expiration
  ) {
    localStorage.removeItem(LOCK_KEY)
    localStorage.removeItem(LOCK_TIMESTAMP_KEY)
    return false
  }

  return localStorage.getItem(LOCK_KEY) === "true"
}

function setLock(lock: boolean): void {
  // console.log("setting lock to: ", lock)
  localStorage.setItem(LOCK_KEY, lock.toString())
  localStorage.setItem(LOCK_TIMESTAMP_KEY, Date.now().toString())
}

function setRefreshActive(active: boolean, hasChanged: boolean): void {
  window.dispatchEvent(
    new CustomEvent("refreshActiveChanged", {
      detail: { active: active, hasChanged: hasChanged },
    })
  )
}

window.addEventListener(
  "refreshActiveChanged",
  (event: CustomEvent<RefreshActiveChangedEventDetail>) => {
    handleRefreshActiveChange(event.detail.active, event.detail.hasChanged)
  }
)

function handleRefreshActiveChange(active: boolean, hasChanged: boolean) {
  startRefreshInterval(hasChanged)
}

function startRefreshInterval(hasChanged: boolean) {
  if (interval) {
    if (hasChanged) clearInterval(interval)
    else return
  }

  const refreshLimit = widget_args.limit
  const refreshInterval = widget_args.interval || 5000

  interval = window.setInterval(() => {
    if (isLocked()) {
      return
    }

    global_count += 1
    const newCount = Math.min(global_count, Number.MAX_SAFE_INTEGER)
    if (!refreshLimit || newCount < refreshLimit) {
      Streamlit.setComponentValue({ action: "update", count: newCount })
    } else {
      clearInterval(interval!)
      interval = null
    }
  }, refreshInterval)
}

function onRender(event: Event): void {
  const data = (event as CustomEvent<RenderData>).detail

  if (data.args.action === "set_lock") {
    setLock(data.args.lock_state === true)
    return
  } else if (data.args.action === "start_refresh") {
    const hasChanged =
      widget_args.setInterval(data.args.interval) ||
      widget_args.setKey(data.args.key) ||
      widget_args.setLimit(data.args.refreshLimit) ||
      widget_args.setLockExpiration(data.args.lock_expiration)
    setRefreshActive(true, hasChanged)
    return
  }
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight(0)
