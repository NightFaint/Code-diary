  Java允许在一个类中定义另一个类，这样的类称为嵌套类。
	
	class OuterClass
	{
	    ...
	    class NestedClass
	    {
	        ...
	    }
	}
	
  嵌套类根据声明时是静态(static)还是非静态(non-static)的又分为两个类型：static nested classes和inner class(non-static
  classes)(内部类)。
  
	class OuterClass
	{
		...
		static class StaticNestedClass
		{
			...
		}
		class InnerClass
		{
			...
		}
	}
	
  嵌套类是外部类的一个成员。内部类对外部类的实例域(可以理解为python中实例的属性)有访问权限，即使这些实例域被定义为
私有的(private)。但是，静态的嵌套类(static nested classes)对外部类的实例域是没有访问权限的。嵌套类可被声明为private,
public，protected。

  使用嵌套类的原因有以下几点：
  
  - 逻辑上，如果一个类只在一个地方使用，那么倾向于把这个类嵌套在我们要用的地方，即另一个类中。
  - 增加了封装性：考虑两个类A和B，如果B需要访问A中被声明为private的实例域，那么把B嵌套在A中可以实现该目的，而不用把A
  的实例域声明为public破坏封装性。另一方面，B嵌套在A中，也使得只有A才能访问B，与外界隔离开来。
  - 增加代码可读性和可维护性。
  
  **Static Nested Classes**
  
  静态的嵌套类通过外部类的类名访问：OuterClass.StaticNestedClass。
  
  例如，创建一个·静态嵌套类对象：
  
	OuterClass.StaticNestedClass nestedObject=new OuterClass.StaticNestedClass();

  **Inner Class**
  
  与实例方法和实例域一样，内部类与一个外部类的实例相关并且对实例方法和实例域有访问权限。
