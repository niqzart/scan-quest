import * as React from "react"

export type CodeLayoutProps = {
  code: string
}

const CodeLayout: React.FC<CodeLayoutProps> = ({ code }) => {
  return <main className="w-screen h-screen content-center text-center p-2">
    <div className="max-w-[600px] m-auto">
      <h1 className="text-3xl font-extrabold tracking-tight text-primary">
        Code Found!
      </h1>
      <h2>
        Found 1/11 codes
      </h2>
      <p>
        {code}
      </p>
      <p>
        Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint Hint
      </p>
    </div>
  </main>
}

export default CodeLayout
