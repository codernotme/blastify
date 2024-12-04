import { Button } from '@/components/ui/button'

interface ActionButtonsProps {
  onClearAll: () => void
}

const ActionButtons: React.FC<ActionButtonsProps> = ({ onClearAll }) => {
  return (
    <div className="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-4">
      <Button variant="outline" onClick={onClearAll} className="w-full sm:w-auto">
        Clear All
      </Button>
      <Button type="submit" className="w-full sm:w-auto">Send Messages</Button>
    </div>
  )
}

export default ActionButtons

