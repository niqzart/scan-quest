import fetcher from "@/api/fetcher"
import { FindingT } from "@/api/types"
import { Card, CardContent, CardDescription, CardTitle } from "@/components/ui/card"
import LoadingSpinner from "@/components/ui/loader"
import * as React from "react"

type FindingCardProps = {
  finding: FindingT
}

const FindingCard: React.FC<FindingCardProps> = ({ finding }) => {
  return <Card className="border-primary">
    <CardContent className="w-full pt-1 pb-2 ">
      <CardTitle>{finding.hint_title}</CardTitle>
      <CardDescription className="text-justify">{finding.hint_content}</CardDescription>
    </CardContent>
  </Card>
}

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

  return <main className="w-screen h-screen text-center p-2 overflow-x-hidden">
    <div className="max-w-[600px] m-auto">
      <h1 className="my-2 scroll-m-20 text-4xl font-extrabold tracking-tight text-primary">
        Findings
      </h1>
      {
        findings === null
          ? <LoadingSpinner size={64} className="text-primary mx-auto" />
          : <div className="space-y-3">
            {findings.map((finding, i) => <div key={i}>
              <FindingCard finding={finding} />
            </div>)}
          </div>
      }
    </div>
  </main>
}

export default FindingsLayout
