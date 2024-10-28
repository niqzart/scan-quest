import fetcher from "@/api/fetcher"
import { FindingT, QuestT } from "@/api/types"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import LoadingSpinner from "@/components/ui/loader"
import * as React from "react"

type SignupFormProps = {
  code: string
  onInvalidCode: () => void
  onSuccess: (finding: FindingT) => void
  quest: QuestT,
}

const SignupForm: React.FC<SignupFormProps> = ({ code, onInvalidCode, onSuccess, quest }) => {
  const [username, setUsername] = React.useState("")
  const [usernameError, setUsernameError] = React.useState(false)

  const onChangeUsername: React.ChangeEventHandler<HTMLInputElement> = (event) => {
    setUsername(event.target.value)
    setUsernameError(false)
  }

  const register = () => {
    fetcher({
      method: "POST",
      path: "public/participants",
      query: { code },
      json: { username },
    }).then(({ response, json }) => {
      if (response.ok) {
        onSuccess(json as FindingT)
      } else if (response.status === 404 && json.detail === "Goal not found") {
        onInvalidCode()
      } else if (response.status === 409 && json.detail === "Username is already taken") {
        setUsernameError(true)
      } else {
        console.error(json)
      }
    }).catch(console.error)
  }

  return <>
    <h1 className="text-3xl font-extrabold tracking-tight text-primary mb-2">
      {quest.welcome_title}
    </h1>
    {quest.welcome_message.split("\n").map((paragraph, i) => (
      <p className="text-justify" key={i}>
        {paragraph}
      </p>
    ))}
    <div className="mt-4 flex w-full items-center space-x-2">
      <Input className={usernameError ? "border-red-500 text-red-500" : ""} type="text" placeholder="Username" value={username} onChange={onChangeUsername} />
      <Button type="submit" onClick={register}>Join</Button>
    </div>
    {usernameError && <p className="text-red-500 text-left text-sm">Username already taken</p>}
  </>
}

export type SignupProps = {
  code: string
  onInvalidCode: () => void
  onSuccess: (finding: FindingT) => void
}

const Signup: React.FC<SignupProps> = ({ code, onInvalidCode, onSuccess }) => {
  const [quest, setQuest] = React.useState<QuestT | null>(null)

  React.useEffect(
    () => {
      if (quest !== null) return
      fetcher({
        path: "public/quests",
        query: { code },
      }).then(({ response, json }) => {
        if (response.ok) {
          setQuest(json as QuestT)
        } else if (response.status === 404 && json.detail === "Goal not found") {
          onInvalidCode()
        } else {
          console.error(json)
        }
      }).catch(console.error)
    }
  )

  return <>
    {quest === null
      ? <LoadingSpinner size={64} className="text-primary mx-auto" />
      : <SignupForm code={code} onInvalidCode={onInvalidCode} onSuccess={onSuccess} quest={quest} />
    }
  </>
}

export default Signup
