from .models import Equipment

def pre_populate_data(app, db):
    newEquipment1 = Equipment(equipment="Bobcat")
    newEquipment2 = Equipment(equipment="Steam roller")
    newEquipment3 = Equipment(equipment="Patch hand roller")
    newEquipment4 = Equipment(equipment="Bull dozer")
    newEquipment5 = Equipment(equipment="Dump Truck")
    newEquipment6 = Equipment(equipment="Power Tamper")
    newEquipment7 = Equipment(equipment="Pro-Patch Asphalt Patcher")
    newEquipment8 = Equipment(equipment="Spray-Injection Machine")
    with app.app_context():
        db.session.add_all([newEquipment1, newEquipment2, newEquipment3, newEquipment4, newEquipment5,
                        newEquipment6, newEquipment7, newEquipment8])

    