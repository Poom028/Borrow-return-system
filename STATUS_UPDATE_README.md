# Status Update Functionality - Returned/Not Returned Dropdown

## Overview
The system now includes a status update functionality that allows users to change the status of borrowed equipment between "Returned" and "Not Returned" using a dropdown interface. This feature automatically manages equipment quantities based on status changes.

## New Features

### 1. Status Dropdown Interface
- **Update Button**: Clicking the "Update" button reveals a status dropdown
- **Status Options**: 
  - "ยังไม่คืน" (Not Returned) - Equipment is still borrowed
  - "คืนแล้ว" (Returned) - Equipment has been returned
- **Cancel Option**: Users can cancel the update operation

### 2. Automatic Equipment Quantity Management
- **Status → "Returned"**: Equipment quantities are restored to available stock
- **Status → "Not Returned"**: Equipment quantities are reduced from available stock
- **Real-time Updates**: Changes are immediately reflected in the equipment display

### 3. Persistent Status Storage
- Status changes are saved to the MongoDB database
- Status persists across page refreshes
- Each note maintains its current return status

## User Interface Changes

### NoteCard Component
```vue
<!-- Status Display -->
<span :class="note.status === 'Returned' ? 'text-green-600' : 'text-red-600'" 
      class="text-sm font-semibold">
  {{ note.status === 'Returned' ? 'คืนแล้ว' : 'ยังไม่คืน' }}
</span>

<!-- Update Button (shows when dropdown is hidden) -->
<button v-if="!showStatusDropdown" 
        @click="showStatusDropdown = true" 
        class="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded text-sm">
  Update
</button>

<!-- Status Dropdown (shows when Update is clicked) -->
<select v-model="selectedStatus" 
        @change="updateStatus" 
        class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm">
  <option value="Not Returned">ยังไม่คืน</option>
  <option value="Returned">คืนแล้ว</option>
</select>

<!-- Cancel Button (shows when dropdown is visible) -->
<button v-if="showStatusDropdown" 
        @click="cancelUpdate" 
        class="bg-gray-500 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm">
  Cancel
</button>
```

## Backend Changes

### 1. Updated Note Model
```python
class Note(Document):
    title = StringField(required=True)
    content = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(User, required=True)
    status = StringField(default="Not Returned", choices=["Returned", "Not Returned"])
```

### 2. Enhanced Update Route
```python
@notes.route("/notes/<note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):
    # Update status
    if "status" in data:
        old_status = note.status
        note.status = data["status"]
        note.save()
        
        # Handle equipment quantity changes
        if old_status == "Not Returned" and data["status"] == "Returned":
            # Restore equipment quantities
            restore_equipment_quantities(note)
        elif old_status == "Returned" and data["status"] == "Not Returned":
            # Reduce equipment quantities
            reduce_equipment_quantities(note)
```

### 3. Smart Equipment Management
- **Status Change Logic**: Equipment quantities are automatically adjusted based on status changes
- **Data Consistency**: Ensures equipment counts remain accurate regardless of status updates
- **Audit Trail**: All quantity changes are logged for debugging

## Data Flow

### 1. Status Update Process
```
User clicks Update → Dropdown appears → User selects status → 
Backend updates note → Equipment quantities adjusted → 
Frontend refreshes → Status persists in database
```

### 2. Equipment Quantity Changes
```
Status: "Not Returned" → "Returned"
- Equipment quantities: +quantity (restored to stock)
- Available stock: Increases

Status: "Returned" → "Not Returned"  
- Equipment quantities: -quantity (reduced from stock)
- Available stock: Decreases
```

### 3. Database Operations
```
1. Update note.status field
2. Parse equipment from note title
3. Adjust equipment quantities based on status change
4. Save all changes atomically
5. Return success response
```

## Frontend Implementation

### 1. State Management
```javascript
const showStatusDropdown = ref(false)
const selectedStatus = ref('')

onMounted(() => {
  selectedStatus.value = props.note.status || 'Not Returned'
})
```

### 2. Update Functions
```javascript
const updateStatus = async () => {
  if (selectedStatus.value !== props.note.status) {
    emit('update', props.note.id, { status: selectedStatus.value })
    showStatusDropdown.value = false
  } else {
    showStatusDropdown.value = false
  }
}

const cancelUpdate = () => {
  selectedStatus.value = props.note.status || 'Not Returned'
  showStatusDropdown.value = false
}
```

### 3. Event Handling
```javascript
// In dashboard.vue
const updateNote = async (id, updatedNote) => {
  await axios.put(`http://localhost:5000/api/notes/${id}`, updatedNote, {
    headers: { Authorization: `Bearer ${token}` }
  })
  fetchNotes() // Refresh notes to get updated status
}
```

## Testing the Functionality

### 1. Start the System
```bash
# Backend
cd backend
python app.py

# Frontend  
cd frontend
npm run dev
```

### 2. Test Status Updates
1. **Login** to the system
2. **Create a note** by borrowing equipment
3. **Click "Update"** on the created note
4. **Select "Returned"** from the dropdown
5. **Verify** equipment quantities are restored
6. **Change back to "Not Returned"**
7. **Verify** equipment quantities are reduced again

### 3. Verify Persistence
1. **Change status** to "Returned"
2. **Refresh the page**
3. **Verify** status remains "Returned"
4. **Check** equipment quantities are still correct

## Debug Output

The backend provides detailed logging for status updates:

### Status Change to "Returned":
```
Updated note 68ae6e2319eab168001c5611 status: Not Returned -> Returned
Restored ลูกเบสบอล: 3 -> 5
```

### Status Change to "Not Returned":
```
Updated note 68ae6e2319eab168001c5611 status: Returned -> Not Returned
Reduced ลูกเบสบอล: 5 -> 3
```

## Benefits

### 1. **User Experience**
- ✅ Intuitive dropdown interface
- ✅ Clear visual feedback
- ✅ Easy status management

### 2. **Data Integrity**
- ✅ Automatic equipment quantity management
- ✅ Consistent status tracking
- ✅ Persistent storage

### 3. **Business Logic**
- ✅ Accurate stock management
- ✅ Return status tracking
- ✅ Equipment availability monitoring

## Future Enhancements

### 1. **Advanced Status Options**
- Partially Returned
- Overdue
- Maintenance Required

### 2. **Status History**
- Track status change history
- Timestamp for each change
- User who made the change

### 3. **Bulk Operations**
- Update multiple notes at once
- Batch status changes
- Bulk equipment quantity updates

### 4. **Notifications**
- Email alerts for returns
- SMS notifications
- Dashboard notifications

## Files Modified

### Backend:
- `backend/models.py` - Added status field to Note model
- `backend/routes/notes.py` - Enhanced update route with status handling

### Frontend:
- `frontend/components/NoteCard.vue` - Added status dropdown interface
- `frontend/pages/dashboard.vue` - Added update event handling

## Summary

The status update functionality provides:
- ✅ **Interactive Dropdown**: Easy status selection between "Returned" and "Not Returned"
- ✅ **Automatic Equipment Management**: Quantities are automatically adjusted based on status
- ✅ **Persistent Storage**: Status changes are saved to the database
- ✅ **Real-time Updates**: Equipment quantities update immediately
- ✅ **User-Friendly Interface**: Intuitive controls with cancel option

Users can now easily track the return status of borrowed equipment and the system automatically manages inventory levels accordingly! 🎉
