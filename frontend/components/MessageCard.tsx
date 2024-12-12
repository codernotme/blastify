import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import MessageInput from './MessageInput'
import { FieldError } from 'react-hook-form'

interface MessageCardProps {
  value: string
  onChange: (value: string) => void
  error?: FieldError
  maxLength?: number // Add maxLength prop
}

const MessageCard: React.FC<MessageCardProps> = ({ value, onChange, error, maxLength }) => {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-xl font-semibold">Compose Message</CardTitle>
      </CardHeader>
      <CardContent>
        <MessageInput value={value} onChange={onChange} error={error} maxLength={maxLength} /> {/* Pass maxLength */}
      </CardContent>
    </Card>
  )
}

export default MessageCard

