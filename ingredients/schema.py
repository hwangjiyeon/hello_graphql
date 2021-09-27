import graphene
from django.db.models import AutoField
from graphene_django.types import DjangoObjectType

from ingredients.models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class Query(object):
    category = graphene.Field(CategoryType,
                              id=graphene.Int(),
                              name=graphene.String())
    all_categories = graphene.List(CategoryType)


    ingredient = graphene.Field(IngredientType,
                                id=graphene.Int(),
                                name=graphene.String())
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.all()

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Category.objects.get(pk=id)

        if name is not None:
            return Category.objects.get(name=name)

        return None

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Ingredient.objects.get(pk=id)

        if name is not None:
            return Ingredient.objects.get(name=name)

        return None


class CreateIngredient(graphene.Mutation):
    # 입력받을 파리미터 Field 정의
    class Arguments:
        name = graphene.String(required=True)
        notes = graphene.String(required=True)
        categoryName = graphene.String(required=True)

    # 반환 Field를 정의
    success = graphene.Boolean()

    # 실행할 Mutation 정의
    def mutate(root, info, **kwargs):
        tempCategoryName = kwargs.get('categoryName')

        try:
            Category.objects.get(name=tempCategoryName)
        except:
            Category( name=tempCategoryName).save()

        categoryObj = Category.objects.get(name=tempCategoryName)

        ingredient = Ingredient(
            name=kwargs.get('name'),
            notes=kwargs.get('notes'),
            category=categoryObj
        )

        # db에 저장
        ingredient.save()

        # 결과 반환
        return CreateIngredient(
            success=True
        )

# update할 필드 정의



class UpdateIngredient(graphene.Mutation):

    class Arguments:
        update_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        notes = graphene.String(required=True)
        category = graphene.Int(required=True)

    # 반환값
    success = graphene.Boolean()

    def mutate(root, info, update_id, name, notes, category):

        # 조회
        model = Ingredient.objects.get(id=update_id)

        # 데이터 수정
        if name is not None:
            model.name = name

        if notes is not None:
            model.notes = notes

        if category is not None:
            model.category = Category( id=category)

        model.save()
        success = True

        return UpdateIngredient(
            success=success
        )

# mutation Field 정의
class Mutation(graphene.ObjectType):
    create_ingredient = CreateIngredient.Field()
    update_ingredient = UpdateIngredient.Field()
