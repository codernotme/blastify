import { useState } from 'react'
import { Textarea } from '@/components/ui/textarea'
import { FieldError } from 'react-hook-form'

interface MessageInputProps {
  value: string
  onChange: (value: string) => void
  error?: FieldError
  maxLength?: number // Add maxLength prop
}

const MessageInput: React.FC<MessageInputProps> = ({ value = '', onChange, error, maxLength }) => { // Default value to empty string
  const [charCount, setCharCount] = useState(value.length) // Initialize with value length

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value
    if (!maxLength || newValue.length <= maxLength) { // Check maxLength
      onChange(newValue)
      setCharCount(newValue.length)
    }
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
        <span className="text-gray-500">{charCount} / {maxLength || '∞'} characters</span> {/* Display maxLength */}
        {error && <span className="text-red-500">{error.message}</span>}
      </div>
    </div>
  )
}

export default MessageInput

