import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import * as React from "react"

const Signup: React.FC = () => {
  const [username, setUsername] = React.useState("")

  const onChangeUsername: React.ChangeEventHandler<HTMLInputElement> = (event) => {
    setUsername(event.target.value)
  }

  const register = () => {
    console.log("Register!", username)
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
      <Input type="text" placeholder="Username" value={username} onChange={onChangeUsername} />
      <Button type="submit" onClick={register}>Join</Button>
    </div>
  </>
}

export default Signup
