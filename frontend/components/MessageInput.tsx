import { useState } from 'react'
import { Textarea } from '@/components/ui/textarea'
import { FieldError } from 'react-hook-form'

interface MessageInputProps {
  value: string
  onChange: (value: string) => void
  error?: FieldError
}

const MessageInput: React.FC<MessageInputProps> = ({ value, onChange, error }) => {
  const [charCount, setCharCount] = useState(0)

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value
    onChange(newValue)
    setCharCount(newValue.length)
  }

  return (
    <div>
      <Textarea
        placeholder="Type your message here..."
        value={value}
        onChange={handleChange}
        className={`min-h-[120px] ${error ? 'border-red-500' : ''}`}
      />
      <div className="flex justify-between mt-2 text-xs sm:text-sm">
        <span className="text-gray-500">{charCount} characters</span>
        {error && <span className="text-red-500">{error.message}</span>}
      </div>
    </div>
  )
}

export default MessageInput

