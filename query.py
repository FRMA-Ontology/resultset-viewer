frma = "https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/"


# treeClassQuery = """
#  select *
#  where{
#      ?class a owl:Class.
#      ?class rdfs:label ?name.
#
#       OPTIONAL {
#        ?class rdfs:subClassOf ?super .
#        ?super a owl:Class.
#           ?super rdfs:label ?super_name.
#       }
#      }
# """

treeClassQuery = """
prefix mlmo: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/>
prefix fibo-fnd-arr-arr: <http://www.omg.org/spec/EDMC-FIBO/FND/Arrangements/Arrangements/>
prefix lio: <http://purl.org/net/lio#>
prefix lcc-lr: <http://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
prefix fibo-fnd-aap-a: <http://www.omg.org/spec/EDMC-FIBO/FND/AgentsAndPeople/Agents/>
prefix img: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/ImageOntology/>
prefix frma: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/>

select distinct ?class ?name ?super ?super_name
 where{
  {
    ?super rdfs:subClassOf ?restriction .
    ?restriction rdf:type owl:Restriction .
    ?restriction owl:someValuesFrom ?class .
	?class a owl:Class.
    ?class rdfs:label ?name.


    bind(<https://w3id.org/lio/v1#Image> AS ?super)
    bind("image" AS ?super_name)
    }
   union
   {
     ?class a owl:Class.
     ?class rdfs:label ?name.
   	 ?class rdfs:subClassOf ?super .

     bind(<https://w3id.org/lio/v1#Image> AS ?super)
     bind("image" AS ?super_name)
     }
   union
   {
     values (?class ?name ?super ?super_name){
     	(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/MugShotPhoto> "mug shot photo" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/ImageOntology/PosedImage> "posed image")
        (<https://w3id.org/lio/v1#PictorialElement> "pictorial element" <https://w3id.org/lio/v1#Image> "image")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Demographic> "demographic" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/WearableThingsOntology/WearableObject> "wearable object" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/VisualDescriptor> "visual descriptor" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<http://purl.obolibrary.org/obo/UBERON_0001567> "cheek" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")

        (<http://purl.obolibrary.org/obo/UBERON_0008199> "chin" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/Hair> "hair" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person" <https://w3id.org/lio/v1#PictorialElement> "pictorial element")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/HairColor> "hair color" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/Hair> "hair")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/HairTexture> "hair texture" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/HeadHair> "head hair")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/Haircut> "haircut" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/HairOntology/HeadHair> "head hair")

        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/FacialExpression> "facial expression" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/FaceShape> "face shape" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
        (<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/SkinTone> "skin tone" <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Person> "person")
     }

     }
   union
   {

     ?class a owl:Class.
      ?class rdfs:label ?name.

       OPTIONAL {
        ?class rdfs:subClassOf ?super .
        ?super a owl:Class.
           ?super rdfs:label ?super_name.
       }
      }

   filter(img:ImageFile != ?class)
   filter(mlmo:Datum != ?super)
   filter(mlmo:Activity != ?super)
   filter(mlmo:Layer != ?super)
   filter(mlmo:Dataset != ?super)
   filter(mlmo:Model != ?super)
   filter(mlmo:NeuralNetwork != ?super)
   filter(<http://purl.obolibrary.org/obo/UBERON_0000475> != ?super)
   filter(<http://purl.obolibrary.org/obo/UBERON_0011676> != ?super)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/ForheadVisibility> != ?super)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/MouthOpenState> != ?super)
   filter(<http://purl.obolibrary.org/obo/UBERON_0001444> != ?super)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/ForheadVisibility> != ?class)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/MouthOpenState> != ?class)

   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Finish> != ?super)
   filter(<http://purl.obolibrary.org/obo/UBERON_0000020> != ?super)
   filter(<http://purl.obolibrary.org/obo/UBERON_0000062> != ?super)

   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Color> != ?super)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Color> != ?class)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/Size> != ?super)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/VisualDescriptor> != ?super)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/VisualDescriptor> != ?class)
   filter(<https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/PersonFaceAndDemographicOntology/NoseShape> != ?super)

} ORDER BY ?super_name ?name
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

baseCountQuery = """
    prefix mlmo: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/MachineLearningModelOntology/>
    prefix fibo-fnd-arr-arr: <http://www.omg.org/spec/EDMC-FIBO/FND/Arrangements/Arrangements/>
    prefix lio: <http://purl.org/net/lio#>
    prefix lcc-lr: <http://www.omg.org/spec/LCC/Languages/LanguageRepresentation/>
    prefix fibo-fnd-aap-a: <http://www.omg.org/spec/EDMC-FIBO/FND/AgentsAndPeople/Agents/>
    prefix img: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/ImageOntology/>
    prefix frma: <https://tw.rpi.edu/Courses/Ontologies/2018/FRMA/FRMA/>

    select (count(distinct ?Image) as ?count)
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
"https://w3id.org/lio/v1#Image" : "",
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
