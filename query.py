frma = "https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/"


treeClassQuery = """
 select *
 where{
     ?class a owl:Class.
     ?class rdfs:label ?name.

      OPTIONAL {
       ?class rdfs:subClassOf ?super .
       ?super a owl:Class.
          ?super rdfs:label ?super_name.
      }
     }
"""


baseQuery = """
    prefix mlmo: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/>
    prefix fibo-fnd-arr-arr: <http://www.omg.org/spec/EDMC-FIBO/FND/Arrangements/Arrangements/>
    prefix lio: <http://purl.org/net/lio#>
    prefix lcc-lr: <http://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
    prefix fibo-fnd-aap-a: <http://www.omg.org/spec/EDMC-FIBO/FND/AgentsAndPeople/Agents/>
    prefix img: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/ImageOntology/>
    prefix frma: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/>

    select distinct ?Image ?classification ?Name
        where {
          ?ResultSet fibo-fnd-arr-arr:hasConstituent ?Result .
          ?Result lcc-lr:hasTag ?classification .
          ?Result mlmo:hasFeature ?Image .
          ?Image lio:depicts ?Person .
          ?Person fibo-fnd-aap-a:hasName ?Name .
"""

mugshotQuery = """
    ?Image a img:PosedImage.

    # Indoors
    ?Image lio:hasDepictedBackground ?background .
    ?background a img:Indoors .

    # No Face occlusions
    OPTIONAL{
      ?Image frma:hasOcclusion ?occlusion.
     }

     minus{
         ?occlusion a ?FaceOcclusionClass .
         ?FaceOcclusionClass rdfs:subClassOf* frma:FaceOcclusion .
     }

    # Image Fidelity not blurry
    ?Image img:fidelityDescribedBy ?fidelity .
    minus{
      ?fidelity a img:BlurryImageFidelity .
     }
"""
occlusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?occlusionClass .
    ?occlusionClass rdfs:subClassOf* frma:Occlusion .
"""

cervicalOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?CervicalOcclusionClass .
    ?CervicalOcclusionClass rdfs:subClassOf* frma:CervicalOcclusion .
"""

FaceOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?FaceOcclusionClass .
    ?FaceOcclusionClass rdfs:subClassOf* frma:FaceOcclusion .
"""

LowerFaceOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?LowerFaceOcclusionClass .
    ?LowerFaceOcclusionClass rdfs:subClassOf* frma:LowerFaceOcclusion .
"""

UpperFaceOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?UpperFaceOcclusionClass .
    ?UpperFaceOcclusionClass rdfs:subClassOf* frma:UpperFaceOcclusion .
"""

BuccalOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?BuccalOcclusionClass .
    ?BuccalOcclusionClass rdfs:subClassOf* frma:BuccalOcclusion .
"""

OralOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?OralOcclusionClass .
    ?OralOcclusionClass rdfs:subClassOf* frma:OralOcclusion .
"""

MentalOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?MentalOcclusionClass .
    ?MentalOcclusionClass rdfs:subClassOf* frma:MentalOcclusion .
"""

ParotidOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?ParotidOcclusionClass .
    ?ParotidOcclusionClass rdfs:subClassOf* frma:ParotidOcclusion .
"""

ZygomaticOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?ZygomaticOcclusionClass .
    ?ZygomaticOcclusionClass rdfs:subClassOf* frma:ZygomaticOcclusion .
"""

AuricleOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?AuricleOcclusionClass .
    ?AuricleOcclusionClass rdfs:subClassOf* frma:AuricleOcclusion .
"""

CranialOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?CranialOcclusionClass .
    ?CranialOcclusionClass rdfs:subClassOf* frma:CranialOcclusion .
"""

FrontalOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?FrontalOcclusionClass .
    ?FrontalOcclusionClass rdfs:subClassOf* frma:FrontalOcclusion .
"""

OcularOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?OcularOcclusionClass .
    ?OcularOcclusionClass rdfs:subClassOf* frma:OcularOcclusion .
"""

NasalOcclusionQuery = """
    ?Image frma:hasOcclusion ?occlusion .
    ?occlusion a ?NasalOcclusionClass .
    ?NasalOcclusionClass rdfs:subClassOf* frma:NasalOcclusion .
"""



querymapper = {
"thing" : "",
frma + "MugShotPhoto": mugshotQuery,
frma + "Occlusion": occlusionQuery,
frma + "CervicalOcclusion" : cervicalOcclusionQuery,
frma + "FaceOcclusion" : FaceOcclusionQuery,
frma + "LowerFaceOcclusion" : LowerFaceOcclusionQuery,
frma + "UpperFaceOcclusion" : UpperFaceOcclusionQuery,
frma + "BuccalOcclusion" : BuccalOcclusionQuery,
frma + "OralOcclusion" : OralOcclusionQuery,
frma + "MentalOcclusion" : MentalOcclusionQuery,
frma + "ParotidOcclusion" : ParotidOcclusionQuery,
frma + "ZygomaticOcclusion" : ZygomaticOcclusionQuery,


frma + "AuricleOcclusion" : AuricleOcclusionQuery,
frma + "CranialOcclusion" : CranialOcclusionQuery,
frma + "FrontalOcclusion" : FrontalOcclusionQuery,
frma + "OcularOcclusion" : OcularOcclusionQuery,
frma + "NasalOcclusion" : NasalOcclusionQuery,

}
