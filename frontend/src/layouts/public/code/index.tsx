import fetcher from "@/api/fetcher"
import { FindingT } from "@/api/types"
import * as React from "react"
import InvalidCode from "./invalid-code"
import Loading from "./loading"
import Signup from "./signup"
import Success from "./success"

export type CodeLayoutProps = {
  code: string
}

type ViewModeT = "loading" | "invalid-code" | "signup" | "success"

const CodeLayout: React.FC<CodeLayoutProps> = ({ code }) => {
  const [viewMode, setViewMode] = React.useState<ViewModeT>("loading")

  const [finding, setFinding] = React.useState<FindingT | null>(null)

  const onInvalidCode = () => setViewMode("invalid-code")
  const onAuthRequired = () => setViewMode("signup")
  const onSuccess = (finding: FindingT) => {
    setFinding(finding)
    setViewMode("success")
  }

  React.useEffect(() => {
    if (viewMode !== "loading") return
    fetcher({
      method: "POST",
      path: "public/participants/me/found-goals",
      query: { code },
    }).then(({ response, json }) => {
      if (response.ok) {
        // TODO get data from newly found goal
        onSuccess(json as FindingT)
      } else if (response.status === 401) {
        onAuthRequired()
      } else if (response.status === 404 && json.detail === "Goal not found") {
        onInvalidCode()
      } else if (response.status === 409 && json.detail === undefined) {
        // TODO show a different message
        onSuccess(json as FindingT)
      } else {
        // TODO error handling
        console.error(json)
      }
    }).catch(console.error)
  })

  return <main className="w-screen h-screen content-center text-center p-2">
    <div className="max-w-[600px] m-auto">
      {viewMode === "loading" && <Loading />}
      {viewMode === "invalid-code" && <InvalidCode />}
      {viewMode === "signup" && <Signup code={code} onInvalidCode={onInvalidCode} onSuccess={onSuccess} />}
      {viewMode === "success" && finding !== null && <Success finding={finding} />}
    </div>
  </main>
}

export default CodeLayout
