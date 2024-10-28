import fetcher from "@/api/fetcher"
import { FindingT } from "@/api/types"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import * as React from "react"

export type SignupProps = {
  code: string
  onInvalidCode: () => void
  onSuccess: (finding: FindingT) => void
}

const Signup: React.FC<SignupProps> = ({ code, onInvalidCode, onSuccess }) => {
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
    <h1 className="text-3xl font-extrabold tracking-tight text-primary">
      Welcome
    </h1>
    <p>
      Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info Quest Info
    </p>
    <h2 className="mt-8 text-primary font-extrabold">
      Let's go?
    </h2>
    <div className="mt-2 flex w-full items-center space-x-2">
      <Input className={usernameError ? "border-red-500 text-red-500" : ""} type="text" placeholder="Username" value={username} onChange={onChangeUsername} />
      <Button type="submit" onClick={register}>Join</Button>
    </div>
    {usernameError && <p className="text-red-500 text-left text-sm">Username already taken</p>}
  </>
}

export default Signup
