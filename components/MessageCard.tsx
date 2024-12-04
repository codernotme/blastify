import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import MessageInput from './MessageInput'
import { FieldError } from 'react-hook-form'

interface MessageCardProps {
  value: string
  onChange: (value: string) => void
  error?: FieldError
}

const MessageCard: React.FC<MessageCardProps> = ({ value, onChange, error }) => {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-xl font-semibold">Compose Message</CardTitle>
      </CardHeader>
      <CardContent>
        <MessageInput value={value} onChange={onChange} error={error} />
      </CardContent>
    </Card>
  )
}

export default MessageCard

