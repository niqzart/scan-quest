export type FindingT = {
  id: string,
  hint_title: string,
  hint_content: string,
}

export type QuestT = {
  id: string,
  name: string,
  welcome_title: string,
  welcome_message: string,
}

export type QuestProgressT = {
  found_goals: number,
  total_goals: number,
}
