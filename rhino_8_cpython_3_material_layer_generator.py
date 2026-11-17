# -*- coding: utf-8 -*-
import os
import clr

clr.AddReference("RhinoCommon")
clr.AddReference("System.Drawing")

import Rhino
import System
import System.Drawing as Drawing

# Exact repository path from your workspace
repo_dir = r"C:\Users\tomas\Dropbox\00_TOMAS\00_PC\01_Work\03_Academic\Arizona\Smarts Cities_Tokyo\vsCode\City-Intelligence"
output_dir = os.path.join(repo_dir, "assets", "materials")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

doc = Rhino.RhinoDoc.ActiveDoc

# Physically Based Material Type GUID in Rhino RDK
pbr_type_id = System.Guid("5a8d7b9b-cdc9-49de-8c16-2ef64fb097ab")

# Shader & Layer Matrix:
# (Material_Name, Layer_Name, Base_RGB, Metallic, Roughness, Emission_RGB, Emission_Mult)
workshop_specs = [
    ("01_Urban_Massing_Slate",     "01_Urban_Massing",  (43, 43, 48),    0.0, 0.85, (0, 0, 0),       0.0),
    ("02_Streets_LightGray",       "02_Street_Network", (185, 190, 200), 0.0, 1.00, (165, 170, 180), 1.0),
    ("03_Acoustic_Pins_Vermilion", "03_Acoustic_Pins",  (224, 79, 51),   0.0, 0.40, (224, 79, 51),   1.2),
    ("04_Braided_Ring_Silver",     "04_Braided_Ring",   (216, 210, 197), 1.0, 0.25, (0, 0, 0),       0.0),
]

def get_or_create_render_material(name, base_rgb, metallic, roughness, em_rgb, em_mult):
    for existing in doc.RenderMaterials:
        if existing.Name == name:
            return existing

    mat = Rhino.Render.RenderContentType.NewContentFromTypeId(pbr_type_id)
    mat.Name = name

    mat.BeginChange(Rhino.Render.RenderContent.ChangeContexts.Program)
    base_col = Rhino.Display.Color4f(Drawing.Color.FromArgb(base_rgb[0], base_rgb[1], base_rgb[2]))
    em_col = Rhino.Display.Color4f(Drawing.Color.FromArgb(em_rgb[0], em_rgb[1], em_rgb[2]))

    mat.SetParameter("base-color", base_col)
    mat.SetParameter("metallic", float(metallic))
    mat.SetParameter("roughness", float(roughness))
    mat.SetParameter("emission", em_col)
    mat.SetParameter("emission-multiplier", float(em_mult))
    mat.EndChange()

    doc.RenderMaterials.Add(mat)
    return mat

def get_or_create_layer(layer_name, display_rgb, render_mat):
    layer_index = doc.Layers.FindByFullPath(layer_name, -1)
    if layer_index < 0:
        layer = Rhino.DocObjects.Layer()
        layer.Name = layer_name
        layer.Color = Drawing.Color.FromArgb(display_rgb[0], display_rgb[1], display_rgb[2])
        layer.RenderMaterial = render_mat
        layer_index = doc.Layers.Add(layer)
    else:
        layer = doc.Layers[layer_index]
        layer.Color = Drawing.Color.FromArgb(display_rgb[0], display_rgb[1], display_rgb[2])
        layer.RenderMaterial = render_mat
        layer.CommitChanges()
    return layer_index

def export_rmtl_file(rmat, filepath):
    # Cast 0 directly to Rhino.Render.RenderContent.EmbedFilesChoice (NoEmbedFiles)
    embed_choice = System.Enum.ToObject(Rhino.Render.RenderContent.EmbedFilesChoice, 0)
    if rmat.SaveToFile(filepath, embed_choice):
        return True

    cmd = '-_RenderSaveMaterialToFile "{0}" "{1}" _Enter'.format(rmat.Name, filepath)
    return Rhino.RhinoApp.RunScript(cmd, False)

for mat_name, layer_name, base_rgb, metallic, roughness, em_rgb, em_mult in workshop_specs:
    rmat = get_or_create_render_material(mat_name, base_rgb, metallic, roughness, em_rgb, em_mult)
    get_or_create_layer(layer_name, base_rgb, rmat)

    rmtl_path = os.path.join(output_dir, "{0}.rmtl".format(mat_name))
    if export_rmtl_file(rmat, rmtl_path):
        print("Serialized RDK material: {0}".format(rmtl_path))
    else:
        print("Material active in document (manual save available via _Materials): {0}".format(mat_name))

doc.Views.Redraw()
print("City Intelligence TOKYO shader & layer setup complete.")