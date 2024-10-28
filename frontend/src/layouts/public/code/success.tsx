import fetcher from "@/api/fetcher"
import { FindingT, QuestProgressT } from "@/api/types"
import LoadingSpinner from "@/components/ui/loader"
import * as React from "react"

export type SuccessProps = {
  finding: FindingT
}

const Success: React.FC<SuccessProps> = ({ finding }) => {
  const [questProgress, setQuestProgress] = React.useState<QuestProgressT | null>(null)

  React.useEffect(() => {
    if (questProgress !== null) return
    fetcher({
      path: "public/participants/me/quest-progress"
    }).then(({ response, json }) => {
      if (response.ok) {
        setQuestProgress(json as QuestProgressT)
      } else {
        // TODO error handling
        console.error(json)
      }
    }).catch(console.error)
  })

  return <>
    <h1 className="text-3xl font-extrabold tracking-tight text-primary mb-2">
      {finding.hint_title}
    </h1>
    {finding.hint_content.split("\n").map((item, key) => (
      <p className="text-justify" key={key}>
        {item}
      </p>
    ))}
    {
      questProgress === null
        ? <LoadingSpinner className="text-primary mx-auto mt-2" size={32} />
        : <h2 className="text-xl font-bold text-primary">Found: {questProgress.found_goals}/{questProgress.total_goals}</h2>
    }
  </>
}

export default Success
