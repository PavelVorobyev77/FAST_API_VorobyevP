from pdb import run
import pyodbc
import uvicorn 
from fastapi import FastAPI, HTTPException


# Connect to SQL Server
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-BK1T0PD\SQLEXPRESS;DATABASE=21.102-08-VP_PM;Trusted_Connection=yes;')
cursor = conn.cursor()


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Get request to retrieve data from the database
@app.get("/get/{material_id}")
async def read_const_material(material_id: int):
    cursor.execute("SELECT * FROM ConstructionMaterials WHERE ID_ConstMaterial=?", material_id)
    row = cursor.fetchone()
    if row:
        return {"material_id": row[0], "material_name": row[1], "quantity": row[2]}
    else:
        raise HTTPException(status_code=404, detail="Material not found")

@app.get("/get_all/")
async def read_all_const_materials():
    cursor.execute("SELECT * FROM ConstructionMaterials")
    rows = cursor.fetchall()
    materials = []
    for row in rows:
        materials.append({"material_id": row[0], "material_name": row[1], "quantity": row[2]})
    return materials

# Set request to add new data to the database
@app.post("/add/")
async def create_const_material(material_id: int,material_name: str, quantity: int):
    cursor.execute("INSERT INTO ConstructionMaterials (ID_ConstMaterial, MaterialName, Quantity) VALUES (?, ?, ?)", material_id, material_name, quantity)
    conn.commit()
    return {"message": "Material added successfully"}


# Update request to modify existing data in the database
@app.put("/update/{material_id}")
async def update_const_material(material_id: int, material_name: str, quantity: int):
    cursor.execute("UPDATE ConstructionMaterials SET MaterialName = ?, Quantity = ? WHERE ID_ConstMaterial = ?", material_name, quantity, material_id)
    conn.commit()
    return {"message": "Material updated successfully"}


# Delete request to remove data from the database
@app.delete("/del/{material_id}")
async def delete_const_material(material_id: int):
    cursor.execute("DELETE FROM ConstructionMaterials WHERE ID_ConstMaterial=?", material_id)
    conn.commit()
    return {"message": "Material deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)