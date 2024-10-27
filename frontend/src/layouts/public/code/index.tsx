import * as React from "react"
import Success from "./success"
import Loading from "./loading"
import Signup from "./signup"

export type CodeLayoutProps = {
  code: string
}

type ViewModeT = "loading" | "signup" | "success"

const CodeLayout: React.FC<CodeLayoutProps> = ({ code }) => {
  const [viewMode, setViewMode] = React.useState<ViewModeT>("loading")

  return <main className="w-screen h-screen content-center text-center p-2">
    <div className="max-w-[600px] m-auto">
      {viewMode === "loading" && <Loading />}
      {viewMode === "signup" && <Signup />}
      {viewMode === "success" && <Success />}
      <p>{code}</p>
    </div>
  </main>
}

export default CodeLayout
