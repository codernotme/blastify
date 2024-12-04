import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import DeliveryMethod from './DeliveryMethod'

interface DeliveryMethodCardProps {
  value: string
  onChange: (value: string) => void
}

const DeliveryMethodCard: React.FC<DeliveryMethodCardProps> = ({ value, onChange }) => {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-xl font-semibold">Delivery Method</CardTitle>
      </CardHeader>
      <CardContent>
        <DeliveryMethod value={value} onChange={onChange} />
      </CardContent>
    </Card>
  )
}

export default DeliveryMethodCard

