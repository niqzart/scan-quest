import fetcher from "@/api/fetcher"
import { FindingT } from "@/api/types"
import LoadingSpinner from "@/components/ui/loader"
import * as React from "react"

const FindingsLayout: React.FC = () => {
  const [findings, setFindings] = React.useState<FindingT[] | null>(null)

  React.useEffect(() => {
    if (findings !== null) return
    fetcher({
      path: "public/participants/me/found-goals",
    }).then(({ response, json }) => {
      if (response.ok) {
        setFindings(json as FindingT[])
      } else {
        // TODO error handling
        console.error(json)
      }
    }).catch(console.error)
  })

  return <main className="w-screen h-screen text-center p-2">
    <div className="max-w-[600px] m-auto">
      <h1 className="mt-2 scroll-m-20 text-4xl font-extrabold tracking-tight text-primary">
        Findings
      </h1>
      {
        findings === null
          ? <LoadingSpinner size={64} className="text-primary mx-auto" />
          : <>
            {findings.map((finding, i) => (
              <div key={i} className="mt-4 flex w-full items-center space-x-2">
                <h4 className="scroll-m-20 text-xl font-semibold tracking-tight">{finding.hint_title}</h4>
                <p>{finding.hint_content}</p>
              </div>
            ))}
          </>
      }
    </div>
  </main>
}

export default FindingsLayout
