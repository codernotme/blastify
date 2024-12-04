import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Label } from '@/components/ui/label'

interface DeliveryMethodProps {
  value: string
  onChange: (value: string) => void
}

const DeliveryMethod: React.FC<DeliveryMethodProps> = ({ value, onChange }) => {
  return (
    <div>
      <RadioGroup value={value} onValueChange={onChange} className="flex flex-col sm:flex-row sm:space-x-4">
        <div className="flex items-center space-x-2 mb-2 sm:mb-0">
          <RadioGroupItem value="whatsapp" id="whatsapp" />
          <Label htmlFor="whatsapp">WhatsApp</Label>
        </div>
        <div className="flex items-center space-x-2">
          <RadioGroupItem value="email" id="email" />
          <Label htmlFor="email">Email</Label>
        </div>
      </RadioGroup>
    </div>
  )
}

export default DeliveryMethod

